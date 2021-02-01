import jwt
import logging

from flask import Blueprint, abort, redirect, request, session, url_for
from flask_login import logout_user
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from modules.base import authentication
from modules.organizations.utils import get_organization_id_for_email
from shared_helpers.config import get_config, get_path_to_oauth_secrets
from shared_helpers import utils


routes = Blueprint('base', __name__,
                   template_folder='../../static/templates')


def get_google_login_url(oauth_redirect_uri=None, redirect_to_after_oauth=None):
  if not oauth_redirect_uri:
    oauth_redirect_uri = '%s%s' % (authentication.get_host_for_request(request),
                                   '/_/auth/oauth2_callback')

  if not redirect_to_after_oauth:
    redirect_to_after_oauth = 'http://localhost:5007' if request.host.startswith('localhost') else '/'

  session['redirect_to_after_oauth'] = str(redirect_to_after_oauth)

  # http://oauth2client.readthedocs.io/en/latest/source/oauth2client.client.html
  flow = flow_from_clientsecrets(get_path_to_oauth_secrets(),
                                 scope='https://www.googleapis.com/auth/userinfo.email',
                                 redirect_uri=oauth_redirect_uri)

  session['oauth_state'] = utils.generate_secret(32)
  try:
    return str(flow.step1_get_authorize_url(state=session['oauth_state']))
  except TypeError:
    # TODO: Fix breakage only appearing in tests.
    return str(flow.step1_get_authorize_url())


@routes.route('/_/auth/login')
def login():
  redirect_to = request.args.get('redirect_to', None)

  return redirect(get_google_login_url(None, redirect_to))


@routes.route('/_/auth/logout')
def logout():
  logout_user()

  return redirect('http://localhost:5007/' if request.host.startswith('localhost') else '/')


def login_via_test_token():
  # used only for end-to-end tests
  if not request.args.get('test_token'):
    return False

  payload = jwt.decode(request.args.get('test_token'), get_config()['testing']['secret'], 'HS256')

  if payload['user_email'].split('@')[1] not in get_config()['testing']['domains']:
    raise Exception('Invalid test user %s, with test token: %s' % (payload['user_email'],
                                                                   request.args.get('test_token')))

  authentication.login_email(payload['user_email'], 'test_token')

  return True


@routes.route('/_/auth/oauth2_callback')
def oauth2_callback():
  try:
    if login_via_test_token():
      return redirect('/')
  except:
    return 'error', 500

  flow = flow_from_clientsecrets(get_path_to_oauth_secrets(),
                                 scope='https://www.googleapis.com/auth/userinfo.email',
                                 redirect_uri=f'{authentication.get_host_for_request(request)}/_/auth/oauth2_callback')

  if not session.get('oauth_state') or session.get('oauth_state') != request.args.get('state'):
    return redirect(url_for('base.login'))

  try:
    credentials = flow.step2_exchange(request.args.get('code'))
  except (FlowExchangeError, ValueError) as e:
    logging.warning(e)
    # user declined to auth; move on
    return redirect(session.get('redirect_to_after_oauth', '/'))

  authentication.login_email(authentication.get_user_email(credentials),
                             'google')

  return redirect(session.get('redirect_to_after_oauth', '/'))


@routes.route('/_/auth/jwt')
def login_with_jwt():
  token = request.args.get('token')

  if not token:
    return abort(400)

  try:
    user_info = jwt.decode(token, get_config()['sessions_secret'], algorithms=['HS256'])

    if get_organization_id_for_email(user_info['email']) != user_info['organization']:
      logging.warning('Attempt to use JWT with mismatched org: %s', token)

      return abort(400)

    authentication.login_email(user_info['email'], user_info['method'])
  except jwt.DecodeError:
    logging.warning('Attempt to use invalid JWT: %s', token)

    return abort(400)
  except jwt.ExpiredSignatureError:
    logging.warning('Attempt to use expired JWT: %s', token)

  return redirect('/')
