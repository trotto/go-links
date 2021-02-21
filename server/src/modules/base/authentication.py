import datetime
import logging
import os
from urllib.parse import quote

from flask import abort, request, redirect
from flask_login import login_user, current_user

from modules.organizations.utils import get_organization_id_for_email
from modules.users.helpers import get_or_create_user, get_user_by_id
from shared_helpers import config
from shared_helpers.services import get as service_get


def login_test_user():
  if os.getenv('ENVIRONMENT') == 'test_env' and request.headers.get('TROTTO_USER_UNDER_TEST'):
    login_user(get_or_create_user(request.headers.get('TROTTO_USER_UNDER_TEST'),
                                  get_organization_id_for_email(request.headers.get('TROTTO_USER_UNDER_TEST'))))


def get_allowed_authentication_methods(organization):
  try:
    return service_get('admin', f'/organizations/{quote(organization)}/settings').get('authentication_methods', None)
  except config.ServiceNotConfiguredError:
    return None


def login(authentication_method, user_id=None, user_email=None):
  if user_id:
    user = get_user_by_id(user_id)

    if not user:
      logging.warning('Attempt to sign in nonexistent user %s', user_id)

      abort(400)
  else:
    user = get_or_create_user(user_email,
                              get_organization_id_for_email(user_email))

  allowed_authentication_methods = get_allowed_authentication_methods(user.organization)
  if allowed_authentication_methods is not None and authentication_method not in allowed_authentication_methods:
    logging.warning("User %s attempted to authenticate with method '%s'. Allowed methods are %s.",
                    user.id, authentication_method, allowed_authentication_methods)

    abort(redirect(f'/_/auth/login?e=auth_not_allowed-{authentication_method}'))

  if not user.accepted_terms_at:
    # all login methods now have UI for consenting to terms
    user.accepted_terms_at = datetime.datetime.utcnow()
    user.put()

  login_user(user)


def validate_user_authentication():
  if current_user and getattr(current_user, 'enabled', None) is False:
    return redirect('/_/auth/login?e=account_disabled')


def get_user_email(oauth_credentials):
  user_info = oauth_credentials.id_token

  if not user_info['email_verified']:
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

  return '%s://%s' % ('http' if host.startswith('localhost:') else 'https',
                      host)
