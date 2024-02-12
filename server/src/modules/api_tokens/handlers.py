from functools import wraps
from typing import Any, Callable, Type

from flask import abort, Blueprint, jsonify
from flask_login import current_user, login_required

from modules.data import get_models
from modules.data.abstract.api_tokens import ApiToken as ApiTokenABC
from modules.data.abstract.users import User
from modules.users.helpers import is_user_admin
from shared_helpers.encoding import convert_entity_to_dict
from shared_helpers.utils import generate_secret


routes = Blueprint('api_tokens', __name__)
ApiToken: Type[ApiTokenABC] = get_models('api_tokens').ApiToken
current_user: User


def _map_response(api_token: ApiTokenABC) -> dict:
  return convert_entity_to_dict(
    api_token,
    ['id', 'key', 'organization', 'revoked'],
    {'revoked': (lambda d: d and str(d).split('+')[0])},
  )


def admin_required(func: Callable) -> Callable:
  @wraps(func)
  @login_required
  def decorated_function(*args, **kwargs) -> Any:
    if not is_user_admin(current_user):
      abort(403)

    return func(*args, **kwargs)

  return decorated_function


@routes.route('/_/api/api_tokens', methods=['POST'])
@admin_required
def create_api_token() -> tuple[dict, int]:
  """Creates API token"""

  api_token = ApiToken(
    key=generate_secret(64),
    organization=current_user.organization,
  )
  api_token.put()

  return _map_response(api_token), 201


@routes.route('/_/api/api_tokens/<id>', methods=['DELETE'])
@admin_required
def revoke_api_token(id: int) -> dict:
  """Revokes API token"""
  api_token = ApiToken.get_by_id(id)
  if not api_token:
    abort(404)
  api_token.revoke()
  
  return _map_response(api_token)


@routes.route('/_/api/api_tokens', methods=['GET'])
@admin_required
def get_api_token_list() -> dict:
  """Gets API token list"""
  return jsonify([
    _map_response(api_token) for api_token in ApiToken.get_list()
  ])
