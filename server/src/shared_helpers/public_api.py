from typing import Callable, Type, Optional
from functools import wraps

from flask import current_app, request, g
from flask_login import current_user

from modules.data import get_models
from modules.data.abstract.api_tokens import ApiToken as ApiTokenABC
from modules.data.abstract.users import User


current_user: User
ApiToken: Type[ApiTokenABC] = get_models('api_tokens').ApiToken


def _get_token_by_key(key: str) -> ApiTokenABC:
  return ApiToken.get_by_key(key)


def get_api_key():
  return request.headers.get('Authorization')


def public_auth() -> Optional[ApiTokenABC]:
  return getattr(g, 'api_token', None)


def login_or_api_token_required(func: Callable) -> Callable:
    """
    Checks user authorization
    The same code as @login_required but with public API check
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Checking for api key
        if key := get_api_key():
          g.api_token = _get_token_by_key(key)

        if request.method in {'OPTIONS'} or current_app.config.get('LOGIN_DISABLED'):
            pass
        elif not current_user.is_authenticated and not public_auth():
            return current_app.login_manager.unauthorized()

        # flask 1.x compatibility
        # current_app.ensure_sync is only available in Flask >= 2.0
        if callable(getattr(current_app, 'ensure_sync', None)):
            return current_app.ensure_sync(func)(*args, **kwargs)
        return func(*args, **kwargs)

    return decorated_view
