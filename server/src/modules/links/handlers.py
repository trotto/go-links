import base64
import datetime
from functools import wraps
import logging
from typing import Any, Optional
from urllib.parse import urlencode

from flask import Blueprint, request, redirect, jsonify, abort, g
from flask_login import current_user, login_required
from jellyfish import levenshtein_distance
import jwt

from modules.base.authentication import login_or_api_token_required, public_auth
from modules.links import helpers
from modules.data import get_models
from modules.organizations.helpers import get_org_edit_mode
from modules.users import helpers as user_helpers
from shared_helpers import config
from shared_helpers.config import get_default_namespace
from shared_helpers.encoding import convert_entity_to_dict
from shared_helpers.events import enqueue_event


routes = Blueprint('links', __name__,
                   template_folder='../../static/templates')


models = get_models('links')


PUBLIC_KEYS = ['id', 'created', 'modified', 'owner', 'namespace',
               'shortpath', 'destination_url', 'type', 'visits_count']


def get_field_conversion_fns():
  return {
    'id': lambda id: str(id),
    'visits_count': (lambda count: count or 0),
    'created': (lambda created: str(created).split('+')[0]),
    'modified': (lambda created: str(created).split('+')[0])
  }


def link_mutation_permission_required(f):
  @wraps(f)
  def decorated_view(*args, **kwargs):
    link = check_mutate_authorization(kwargs['link_id'])
    if not link:
      abort(403)

    g.link = link

    return f(*args, **kwargs)

  return decorated_view


def check_mutate_authorization(link_id, user_id=None):
  try:
    existing_link = models.ShortLink.get_by_id(link_id)
  except Exception as e:
    logging.warning(str(e))

    return False

  if public_auth():
    return existing_link

  if user_id:
    user = user_helpers.get_user_by_id(user_id)
  else:
    user = current_user

  if not existing_link:
    return False

  if user.organization != existing_link.organization:
    return False

  if existing_link.owner == user.email:
    return existing_link
  elif user_helpers.is_user_admin(user):
    return existing_link
  # allow any user in org to edit a link's destination if the org's edit mode is `any_org_user`
  elif request.method.upper() == 'PUT' and request.json:
    update_keys = list(request.json.keys())
    if (len(update_keys) == 1 and update_keys[0] == 'destination'
        and get_org_edit_mode(user.organization) == 'any_org_user'):
      return existing_link

  return False


def _get_link_response(link):
  link_response = convert_entity_to_dict(link, PUBLIC_KEYS, get_field_conversion_fns())

  link_response['shortpath'] = getattr(link, 'display_shortpath') or link_response['shortpath']

  return link_response


def _order_links_by_similarity(
  links: list[dict[str, Any]],
  similar_to: str,
  similarity_threshold: Optional[float],
  ) -> list[dict[str, Any]]:
  distances = {link['id']: levenshtein_distance(similar_to, link['shortpath']) / len(link['shortpath'])
               for link in links}
  if similarity_threshold:
    links = [link for link in links
             if distances[link['id']] <= similarity_threshold]
  return sorted(links, key=lambda link:distances[link['id']])


def _get_organization() -> str:
  """Gets organization based on auth type"""
  if token := public_auth():
    return token.organization
  return current_user.organization


@routes.route('/_/api/links', methods=['GET'])
@login_or_api_token_required
def get_links():
  similar_to = request.args.get('similar_to')
  limit = request.args.get('limit', type=int)
  similarity_threshold = request.args.get('similarity_threshold', type=float)

  links = [_get_link_response(entity)
           for entity in helpers.get_all_shortlinks_for_org(_get_organization())]

  if not public_auth():
    for link in links:
      link['mine'] = link['owner'] == current_user.email

  if similar_to:
    links = _order_links_by_similarity(links, similar_to, similarity_threshold)

  if limit:
    links = links[:limit]

  return jsonify(links)


@routes.route('/_/api/links', methods=['POST'])
@login_or_api_token_required
def post_link():
  object_data = request.json

  owner = object_data.get('owner')
  acting_user = current_user

  if public_auth():
    if not owner:
      abort(400)
    acting_user = None
  else:
    if owner and not user_helpers.is_user_admin(current_user):
      abort(403)
    owner = owner or current_user.email

  try:
    new_link = helpers.create_short_link(acting_user,
                                         _get_organization(),
                                         owner,
                                         object_data.get('namespace', get_default_namespace(_get_organization())),
                                         object_data['shortpath'],
                                         object_data['destination'],
                                         request.args.get('validation', helpers.SIMPLE_VALIDATION_MODE))
  except helpers.LinkCreationException as e:
    return jsonify({
      'error': str(e)
    })

  logging.info(f'{acting_user.email if acting_user else _get_organization()} created go link with ID {new_link.id}')

  return jsonify(
    _get_link_response(new_link)
  ), 201


@routes.route('/_/api/links/<link_id>', methods=['PUT'])
@login_or_api_token_required
@link_mutation_permission_required
def put(link_id):
  existing_link = g.link

  object_data = request.json

  existing_link.destination_url = object_data['destination']

  acting_user = current_user if not public_auth() else None

  try:
    return jsonify(_get_link_response(helpers.update_short_link(acting_user, existing_link)))
  except helpers.LinkCreationException as e:
    return jsonify({
      'error': str(e),
      'error_type': 'error_bar'
    })


@routes.route('/_/api/links/<link_id>', methods=['DELETE'])
@login_or_api_token_required
@link_mutation_permission_required
def delete(link_id):
  existing_link = g.link

  logging.info('Deleting link: %s' % (convert_entity_to_dict(existing_link, PUBLIC_KEYS)))

  existing_link.delete()

  enqueue_event(existing_link.organization,
                'link.deleted',
                'link',
                _get_link_response(existing_link))

  return jsonify({})


@routes.route('/_/api/links/<link_id>/transfer_link', methods=['POST'])
@link_mutation_permission_required
@login_required
def create_transfer_link(link_id):
  TOKEN_DURATION_IN_HOURS = 24

  payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_DURATION_IN_HOURS),
             'sub': f'link:{link_id}',
             'tp': 'transfer',  # "tp" -> token permissions
             'o': user_helpers.get_or_create_user(g.link.owner, g.link.organization).id,  # "o" -> link owner
             'by': current_user.id}

  token = jwt.encode(payload, config.get_config()['sessions_secret'], algorithm='HS256').encode('utf-8')

  full_url = f"{request.host_url}_transfer/{base64.urlsafe_b64encode(token).decode('utf-8').strip('=')}"

  return jsonify({'url': full_url}), 201


class InvalidTransferToken(Exception):
  pass


@routes.route('/_/api/transfer_link/<transfer_link_token>', methods=['POST'])
@login_required
def use_transfer_link(transfer_link_token):
  user_facing_error = None

  try:
    padded_token = transfer_link_token + '=' * (4 - len(transfer_link_token) % 4)  # add any missing base64 padding

    payload = jwt.decode(base64.urlsafe_b64decode(padded_token),
                         config.get_config()['sessions_secret'],
                         'HS256')
  except (jwt.exceptions.ExpiredSignatureError,
          jwt.exceptions.InvalidSignatureError,
          jwt.exceptions.DecodeError) as e:
    if type(e) is jwt.exceptions.ExpiredSignatureError:
      user_facing_error = 'Your transfer link has expired'

      logging.info('Attempt to use expired token: %s', transfer_link_token)
    if type(e) is jwt.exceptions.InvalidSignatureError:
      logging.warning('Attempt to use invalid token: %s', transfer_link_token)

    abort(403, user_facing_error or 'Your transfer link is no longer valid')

  try:
    if not payload['sub'].startswith('link:'):
      raise InvalidTransferToken('Subject is not link')

    if 'transfer' != payload['tp']:
      raise InvalidTransferToken('Invalid token permission')

    link_id = int(payload['sub'][len('link:'):])
    link = models.ShortLink.get_by_id(link_id)
    if not link:
      raise InvalidTransferToken('Link does not exist')

    owner_from_token = user_helpers.get_user_by_id(payload['o'])
    if not owner_from_token or link.owner != owner_from_token.email:
      user_facing_error = f'The owner of {link.namespace}/{link.shortpath} has changed since your transfer link was created'

      raise InvalidTransferToken('Owner from token does not match current owner')

    if not check_mutate_authorization(link_id, payload['by']):
      user_facing_error = f'The user who created your transfer link no longer has edit rights for {link.namespace}/{link.shortpath}'

      raise InvalidTransferToken('Token from unauthorized user')

    if current_user.organization != link.organization:
      raise InvalidTransferToken("Current user does not match link's organization")
  except (InvalidTransferToken,
          KeyError) as e:
    logging.warning(e)
    logging.warning('Attempt to use invalid token: %s', transfer_link_token)

    abort(403, user_facing_error or 'Your transfer link is no longer valid')

  link.owner = current_user.email
  link.put()

  return '', 201


@routes.route('/_transfer/<transfer_link_token>')
def redirect_transfer_url(transfer_link_token):
  if not current_user.is_authenticated:
    return redirect(f"/_/auth/login?{urlencode({'redirect_to': request.full_path})}")

  return redirect(f"/?{urlencode({'transfer': transfer_link_token})}")
