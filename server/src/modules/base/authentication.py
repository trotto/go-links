import os

from flask import request
from flask_login import login_user

from modules.organizations.utils import get_organization_id_for_email
from modules.users.helpers import get_or_create_user


def login_test_user():
  if os.getenv('ENVIRONMENT') == 'test_env' and request.headers.get('TROTTO_USER_UNDER_TEST'):
    login_user(get_or_create_user(request.headers.get('TROTTO_USER_UNDER_TEST'),
                                  get_organization_id_for_email(request.headers.get('TROTTO_USER_UNDER_TEST'))))


def get_user_email(oauth_credentials):
  user_info = oauth_credentials.id_token

  if not user_info['email_verified']:
    return None

  return user_info['email'].lower()


def get_host_for_request(request):
  return 'https://%s' % (request.headers.get('X-Upstream-Host') or request.host)
