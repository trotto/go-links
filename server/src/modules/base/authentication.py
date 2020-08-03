import httplib2
import os

from apiclient.discovery import build
from flask import request
from flask_login import login_user

from modules.organizations.utils import get_organization_id_for_email
from modules.users.helpers import get_or_create_user


def login_test_user():
  if os.getenv('ENVIRONMENT') == 'test_env' and request.headers.get('TROTTO_USER_UNDER_TEST'):
    login_user(get_or_create_user(request.headers.get('TROTTO_USER_UNDER_TEST'),
                                  get_organization_id_for_email(request.headers.get('TROTTO_USER_UNDER_TEST'))))


def get_user_email(oauth_credentials):
  http = httplib2.Http()
  http = oauth_credentials.authorize(http)

  user_info = build('oauth2', 'v2').tokeninfo().execute(http)

  if not user_info['verified_email']:
    return None

  return user_info['email'].lower()


def get_host_for_request(request):
  return 'https://%s' % (request.headers.get('X-Upstream-Host') or request.host)
