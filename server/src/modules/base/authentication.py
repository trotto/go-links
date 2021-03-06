import datetime
import logging
import os

from flask import abort, request, redirect
from flask_login import login_user, current_user

from modules.organizations.utils import get_organization_id_for_email
from modules.users.helpers import get_or_create_user
from shared_helpers import config
from shared_helpers.services import get as service_get


def login_test_user():
  if os.getenv('ENVIRONMENT') == 'test_env' and request.headers.get('TROTTO_USER_UNDER_TEST'):
    login_user(get_or_create_user(request.headers.get('TROTTO_USER_UNDER_TEST'),
                                  get_organization_id_for_email(request.headers.get('TROTTO_USER_UNDER_TEST'))))


def get_allowed_authentication_methods(organization):
  try:
    return service_get('admin', f'/organizations/{organization}/settings').get('authentication_methods', None)
  except config.ServiceNotConfiguredError:
    return None


def login_email(user_email, authentication_method):
  user = get_or_create_user(user_email,
                            get_organization_id_for_email(user_email))

  allowed_authentication_methods = get_allowed_authentication_methods(user.organization)
  if allowed_authentication_methods is not None and authentication_method not in allowed_authentication_methods:
    logging.warning("User %s attempted to authenticate with method '%s'. Allowed methods are %s.",
                    user_email, authentication_method, allowed_authentication_methods)

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

  return user_info['email'].lower()


def get_host_for_request(request):
  host = request.headers.get('X-Upstream-Host') or request.host

  return '%s://%s' % ('http' if host.startswith('localhost:') else 'https',
                      host)
