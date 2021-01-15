import copy

from flask import Blueprint, request, jsonify, abort
from flask_login import current_user, login_required

from modules.users.helpers import get_users_by_organization, is_user_admin, get_user_by_id


routes = Blueprint('users', __name__,
                   template_folder='../../static/templates')


def _user_info(user):
  return {
    'id': user.id,
    'created': user.created.isoformat()[:19],
    'email': user.email,
    'organization': user.organization,
    'admin': is_user_admin(user),
    'role': user.role,
    'notifications': user.notifications or {}
  }


@routes.route('/_/api/users/<user_id>', methods=['GET'])
@login_required
def get_user(user_id):
  if user_id == 'me':
    return jsonify(_user_info(current_user))

  user = get_user_by_id(int(user_id))

  if not user or not is_user_admin(copy.copy(current_user), user.organization):
    abort(403)

  return jsonify(_user_info(user))


@routes.route('/_/api/organizations/mine/users', methods=['GET'])
@login_required
def get_my_org_users():
  if not is_user_admin(copy.copy(current_user)):
    abort(403)

  return jsonify([_user_info(u) for u in get_users_by_organization(current_user.organization)])


@routes.route('/_/api/users/me', methods=['PUT'])
@login_required
def put_me():
  request_data = request.json

  current_user.notifications = current_user.notifications or {}
  current_user.notifications.update(request_data.get('notifications', {}))

  current_user.put()

  return jsonify(_user_info(current_user))
