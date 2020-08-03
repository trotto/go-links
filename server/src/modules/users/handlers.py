from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from modules.users.helpers import is_user_admin


routes = Blueprint('users', __name__,
                   template_folder='../../static/templates')


def _user_info(user):
  return {
    'email': user.email,
    'admin': is_user_admin(user),
    'role': user.role,
    'notifications': user.notifications or {}
  }


@routes.route('/_/api/users/me', methods=['GET'])
@login_required
def get_me():
  return jsonify(_user_info(current_user))


@routes.route('/_/api/users/me', methods=['PUT'])
@login_required
def put_me():
  request_data = request.json

  current_user.notifications = current_user.notifications or {}
  current_user.notifications.update(request_data.get('notifications', {}))

  current_user.put()

  return jsonify(_user_info(current_user))
