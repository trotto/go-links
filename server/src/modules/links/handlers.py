import logging

from flask import Blueprint, request, jsonify, abort
from flask_login import current_user, login_required

from modules.links import helpers
from modules.data import get_models
from modules.users import helpers as user_helpers
from shared_helpers.encoding import convert_entity_to_dict
from shared_helpers.events import enqueue_event


routes = Blueprint('links', __name__,
                   template_folder='../../static/templates')


models = get_models('links')


PUBLIC_KEYS = ['id', 'created', 'modified', 'owner', 'shortpath', 'destination_url', 'visits_count']


def get_field_conversion_fns():
  return {
    'visits_count': (lambda count: count or 0),
    'created': (lambda created: str(created).split('+')[0]),
    'modified': (lambda created: str(created).split('+')[0])
  }


def check_authorization(link_id):
  try:
    existing_link = models.ShortLink.get_by_id(link_id)
  except Exception as e:
    logging.warning(str(e))

    return False

  if not existing_link:
    return False

  if (existing_link.owner != current_user.email
      and not (current_user.organization == existing_link.organization
               and user_helpers.is_user_admin(current_user))):
    return False

  return existing_link


def _get_link_response(link):
  return convert_entity_to_dict(link, PUBLIC_KEYS, get_field_conversion_fns())


@routes.route('/_/api/links', methods=['GET'])
@login_required
def get_links():
  links = [convert_entity_to_dict(entity, PUBLIC_KEYS, get_field_conversion_fns())
           for entity in helpers.get_all_shortlinks_for_org(current_user.organization)]

  for link in links:
    link['mine'] = link['owner'] == current_user.email

  return jsonify(links)


@routes.route('/_/api/links', methods=['POST'])
@login_required
def post_link():
  object_data = request.json

  if 'owner' in object_data and not user_helpers.is_user_admin(current_user):
    return abort(403)

  try:
    new_link = helpers.create_short_link(current_user.organization,
                                         object_data.get('owner', current_user.email),
                                         object_data['shortpath'],
                                         object_data['destination'])
  except helpers.LinkCreationException as e:
    return jsonify({
      'error': str(e)
    })

  logging.info(f'{current_user.email} created go link with ID {new_link.id}')

  return jsonify(
    convert_entity_to_dict(new_link, PUBLIC_KEYS, get_field_conversion_fns())
  ), 201


@routes.route('/_/api/links/<link_id>', methods=['PUT'])
@login_required
def put(link_id):
  existing_link = check_authorization(link_id)

  if not existing_link:
    return abort(403)

  object_data = request.json

  existing_link.destination_url = object_data['destination']

  try:
    return jsonify(_get_link_response(helpers.update_short_link(existing_link)))
  except helpers.LinkCreationException as e:
    return jsonify({
      'error': str(e),
      'error_type': 'error_bar'
    })


@routes.route('/_/api/links/<link_id>', methods=['DELETE'])
@login_required
def delete(link_id):
  existing_link = check_authorization(link_id)

  if not existing_link:
    return abort(403)

  logging.info('Deleting link: %s' % (convert_entity_to_dict(existing_link, PUBLIC_KEYS)))

  existing_link.delete()

  enqueue_event('link.deleted',
                'link',
                convert_entity_to_dict(existing_link, PUBLIC_KEYS, get_field_conversion_fns()))

  return jsonify({})
