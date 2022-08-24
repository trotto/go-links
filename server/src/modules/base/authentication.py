import datetime
import logging
import os
from urllib.parse import quote

from flask import abort, request, redirect, session
from flask_login import login_user, current_user
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError

from modules.organizations.utils import get_organization_id_for_email
from modules.users.helpers import get_or_create_user, get_user_by_id
from shared_helpers import config
from shared_helpers.services import validate_internal_request, get as service_get, InvalidInternalToken

try:
  from commercial.auth import handle_unsupported_signin
except ModuleNotFoundError:
  handle_unsupported_signin = None


ADDITIONAL_ALLOWED_ORIGINS = config.get_config_by_key_path(['additional_allowed_origins']) or []


csrf_exempt_paths = set()


def login_test_user():
  if os.getenv('ENVIRONMENT') == 'test_env' and request.headers.get('TROTTO_USER_UNDER_TEST'):
    login_user(get_or_create_user(request.headers.get('TROTTO_USER_UNDER_TEST'),
                                  get_organization_id_for_email(request.headers.get('TROTTO_USER_UNDER_TEST'))))
    session['last_signin'] = datetime.datetime.utcnow()


def check_csrf():
  """Verifies one of the following is true, or aborts with 400.

  a) the request includes a valid CSRF token
  b) the origin is explicitly allowed
  c) the request includes a valid internal token
  """
  if request.method in ['OPTIONS', 'GET']:
    return

  try:
    validate_csrf(request.headers.get('X-CSRFToken'))

    return
  except ValidationError:
    pass

  if request.headers.get('origin') in ADDITIONAL_ALLOWED_ORIGINS:
    return

  if request.path in csrf_exempt_paths:
    return

  try:
    validate_internal_request(request)

    return
  except InvalidInternalToken:
    pass

  abort(400, 'Invalid CSRF token.')


def exempt_path_from_csrf(path):
  csrf_exempt_paths.add(path)


def get_allowed_authentication_methods(organization):
  try:
    return service_get('admin', f'/organizations/{quote(organization)}/settings').get('authentication_methods', None)
  except config.ServiceNotConfiguredError:
    return None

"""At least `user_id` or `user_email` must be provided.

If only `user_email` is provided, the `user_org` will be derived from the email. The caller MUST
verify that the `user_email` has been validated by the identity provider, e.g., by checking the
'email_verified' property of an identity token from Google.
"""
def login(authentication_method, user_id=None, user_email=None, user_org=None):
  if not user_id and not user_email:
    abort(400)

  if user_id:
    user = get_user_by_id(user_id)

    if not user:
      logging.warning('Attempt to sign in nonexistent user %s', user_id)

      abort(400)
  else:
    user = get_or_create_user(user_email,
                              user_org if user_org else get_organization_id_for_email(user_email))

  allowed_authentication_methods = get_allowed_authentication_methods(user.organization)
  if allowed_authentication_methods is not None and authentication_method not in allowed_authentication_methods:
    logging.warning("User %s attempted to authenticate with method '%s'. Allowed methods are %s.",
                    user.id, authentication_method, allowed_authentication_methods)

    unsupported_signin_redirect = f'/_/auth/login?e=auth_not_allowed-{authentication_method}'

    if handle_unsupported_signin is not None:
      redirect_override = handle_unsupported_signin(user.organization,
                                                    authentication_method,
                                                    allowed_authentication_methods)

      if redirect_override:
        unsupported_signin_redirect = redirect_override

    abort(redirect(unsupported_signin_redirect))

  if not user.accepted_terms_at:
    # all login methods now have UI for consenting to terms
    user.accepted_terms_at = datetime.datetime.utcnow()
    user.put()

  login_user(user)
  session['last_signin'] = datetime.datetime.utcnow()


def validate_user_authentication():
  if current_user and getattr(current_user, 'enabled', None) is False:
    return redirect('/_/auth/login?e=account_disabled')


def get_user_email(oauth_credentials):
  user_info = oauth_credentials.id_token

  email_verified = user_info['email_verified']

  if type(email_verified) is not bool:
    raise Exception(f"'email_verified' property is wrong type ({type(email_verified).__name__}). Should be bool.")

  if not email_verified:
    return None

  user_email = user_info['email'].lower()

  _, domain = user_email.split('@', 1)

  # Only permit Google auth for Gmail or Google Workspace (fka G Suite) accounts.
  # See go/1199638960374226.
  if domain != 'gmail.com' and not user_info.get('hd'):
    logging.warning('Unsupported Google login for email %s', user_email)

    return None

  return user_email


def get_host_for_request(request):
  host = request.headers.get('X-Upstream-Host') or request.host

  return '%s://%s' % ('http' if host == 'localhost' or host.startswith('localhost:') else 'https',
                      host)
