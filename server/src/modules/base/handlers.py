import jwt
import logging
from urllib.parse import urlencode

from flask import Blueprint, Response, abort, redirect, render_template, request, session, url_for, make_response
from flask_login import logout_user
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from modules.base import authentication, errors
from modules.organizations.utils import get_organization_id_for_email
from shared_helpers.config import get_config, get_path_to_oauth_secrets, get_config_by_key_path
from shared_helpers import config, utils, feature_flags


LOGIN_METHODS = [{'label': 'Sign in with Google',
                  'image': '/_images/auth/google_signin_button.png',
                  'url': '/_/auth/login/google'}
                 ] + (get_config_by_key_path(['authentication', 'methods']) or [])


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
  redirect_to = authentication.get_host_for_request(request)
  if request.args.get('redirect_to', None):
    redirect_to += request.args.get('redirect_to', None)

  error_message = None
  if request.args.get('e', None):
    error_message = errors.get_error_message_from_code(request.args.get('e', None))

  if error_message or len(LOGIN_METHODS) > 1:
    if feature_flags.provider.get('new_frontend'):
      return render_template('_next_static/login.html')

    response = render_template('auth/login_selector.html',
                           login_methods=LOGIN_METHODS,
                           redirect_to=urlencode({'redirect_to': redirect_to}),
                           error_message=error_message)
    response = make_response(response)
    response.headers['Content-Security-Policy'] = (
      "default-src 'self'; "
      "script-src 'self' ajax.googleapis.com; "
      "style-src 'self' fonts.googleapis.com maxcdn.bootstrapcdn.com 'unsafe-inline'; "
      "font-src fonts.gstatic.com maxcdn.bootstrapcdn.com; "
      "base-uri 'self';"
    )

    return response

  return redirect(f"/_/auth/login/google?{urlencode({'redirect_to': redirect_to})}")


@routes.route('/_/auth/logout')
def logout():
  logout_user()

  return redirect('http://localhost:5007/' if request.host.startswith('localhost') else '/')


@routes.route('/_/auth/login/google')
def login_google():
  return redirect(get_google_login_url(None, request.args.get('redirect_to', None)))


def login_via_test_token():
  # used only for end-to-end tests
  if not request.args.get('test_token'):
    return False

  payload = jwt.decode(request.args.get('test_token'), get_config()['testing']['secret'], 'HS256')

  if payload['user_email'].split('@')[1] not in get_config()['testing']['domains']:
    raise Exception('Invalid test user %s, with test token: %s' % (payload['user_email'],
                                                                   request.args.get('test_token')))

  authentication.login('test_token', user_email=payload['user_email'])

  return True


def _redirect():
  if session.get('redirect_to_after_oauth', '').startswith(authentication.get_host_for_request(request) + '/'):
    return redirect(session.get('redirect_to_after_oauth'))

  return redirect('/')


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
    return _redirect()

  user_email = authentication.get_user_email(credentials)

  if user_email:
    authentication.login('google', user_email=user_email)

  return _redirect()


@routes.route('/_/auth/jwt')
def login_with_jwt():
  token = request.args.get('token')

  if not token:
    return abort(400)

  try:
    user_info = jwt.decode(token, get_config()['sessions_secret'], algorithms=['HS256'])

    if 'id' not in user_info and not ('email' in user_info and 'organization' in user_info):
      return abort(400)

    if 'id' in user_info:
      authentication.login(user_info['method'], user_id=user_info['id'])
    else:
      authentication.login(user_info['method'], user_email=user_info['email'], user_org=user_info['organization'])
  except jwt.DecodeError:
    logging.warning('Attempt to use invalid JWT: %s', token)

    return abort(400)
  except jwt.ExpiredSignatureError:
    logging.warning('Attempt to use expired JWT: %s', token)

  redirect_to = authentication.get_host_for_request(request)
  if request.args.get('redirect_to', '').startswith(redirect_to + '/'):
    redirect_to = request.args['redirect_to']

  return redirect(redirect_to)


@routes.route('/_/opensearch')
def opensearch():
  return Response(response=render_template('opensearch/manifest.xml'),
                  status=200,
                  mimetype="application/opensearchdescription+xml")

