import copy

from flask import Blueprint, request, jsonify, abort
from flask_login import current_user, login_required

from modules.links.helpers import get_keyword_validation_regex
from modules.organizations.helpers import get_org_edit_mode
from modules.users.helpers import get_users_by_organization, is_user_admin, get_user_by_id, get_admin_ids
from shared_helpers.config import get_organization_config


routes = Blueprint('users', __name__,
                   template_folder='../../static/templates')


def _user_info(user, admins_ids=None, org_edit_mode=None, org_settings=None):
  user_info = {
    'id': user.id,
    'created': user.created.isoformat()[:19],
    'email': user.email,
    'organization': user.organization,
    'admin': user.id in admins_ids if admins_ids is not None else is_user_admin(user),
    'role': user.role,
    'notifications': user.notifications or {}
  }

  if org_settings is not None:
    user_info.update({
      'read_only_mode': org_settings.get('read_only_mode'),
      'info_bar': org_settings.get('info_bar'),
      'keywords_validation_regex': get_keyword_validation_regex(org_settings)
    })

  if org_edit_mode:
    user_info['org_edit_mode'] = org_edit_mode

  return user_info


@routes.route('/_/api/users/<user_id>', methods=['GET'])
@login_required
def get_user(user_id):
  if user_id == 'me':
    org_edit_mode = get_org_edit_mode(current_user.organization)
    org_settings = get_organization_config(current_user.organization)

    return jsonify(_user_info(current_user, None, org_edit_mode, org_settings))

  user = get_user_by_id(int(user_id))

  if not user or not is_user_admin(copy.copy(current_user), user.organization):
    abort(403)

  return jsonify(_user_info(user))


@routes.route('/_/api/organizations/mine/users', methods=['GET'])
@login_required
def get_my_org_users():
  if not is_user_admin(copy.copy(current_user)):
    abort(403)

  admin_ids = get_admin_ids(current_user.organization)

  return jsonify([_user_info(u, admin_ids)
                  for u in get_users_by_organization(current_user.organization)])


@routes.route('/_/api/users/me', methods=['PUT'])
@login_required
def put_me():
  request_data = request.json

  current_user.notifications = current_user.notifications or {}
  current_user.notifications.update(request_data.get('notifications', {}))

  current_user.put()

  return jsonify(_user_info(current_user))
