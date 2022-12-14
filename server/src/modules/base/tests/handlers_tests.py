import datetime
from urllib.parse import urlencode

from flask import Blueprint, jsonify
import jwt
from mock import patch

from modules.base import handlers
from modules.data import get_models
from testing import TrottoTestCase


User = get_models('users').User


MULTIPLE_LOGIN_METHODS = [{'label': 'Sign in with Google',
                           'image': '/_images/auth/google_signin_button.png',
                           'url': '/_/auth/login/google'},
                          {'label': 'Custom signin',
                           'image': 'https://mylogin/logo.png',
                           'url': 'https://mylogin/login'}]


test_blueprint = Blueprint('test', __name__)

@test_blueprint.route('/me')
def get_me():
  from flask_login import current_user

  return jsonify({'email': current_user.email,
                  'org': current_user.organization})


class AuthenticationTestCase(TrottoTestCase):

  blueprints_under_test = [handlers.routes,
                           test_blueprint]

  def _assert_authentication_status(self, login_response, authenticated, expected_user_email=None, expected_user_org=None):
    user_info_response = self.testapp.get('/me',
                                          headers={'Cookie': login_response.headers['Set-Cookie']},
                                          expect_errors=not authenticated)

    self.assertEqual(200 if authenticated else 500, user_info_response.status_code)
    if authenticated:
      self.assertEqual({'email': expected_user_email,
                        'org': expected_user_org},
                       user_info_response.json)


class TestHandlers(AuthenticationTestCase):

  def test_login_endpoint__no_upstream_host_header(self):
    response = self.testapp.get('/_/auth/login/google',
                                headers={'Host': 'trot.to'})

    expected_oauth_redirect_uri = urlencode({'redirect_uri': 'https://trot.to/_/auth/oauth2_callback'})

    self.assertEqual(302, response.status_int)
    self.assertIn(expected_oauth_redirect_uri, response.headers['Location'])

  def test_login_endpoint__upstream_host_header(self):
    response = self.testapp.get('/_/auth/login/google',
                                headers={'Host': 'trot.to',
                                         'X-Upstream-Host': 'go.trot.to'})

    expected_oauth_redirect_uri = urlencode({'redirect_uri': 'https://go.trot.to/_/auth/oauth2_callback'})

    self.assertEqual(302, response.status_int)
    self.assertIn(expected_oauth_redirect_uri, response.headers['Location'])

  def test_login_endpoint__with_error_code(self):
    response = self.testapp.get('/_/auth/login?e=account_disabled')

    self.assertEqual(200, response.status_int)
    self.assertIn('error-bar', response.text)

  def test_login_endpoint__with_unknown_error_code(self):
    response = self.testapp.get('/_/auth/login?e=mysterycode')

    self.assertEqual(302, response.status_int)

  def test_login_endpoint__single_login_method(self):
    response = self.testapp.get('/_/auth/login')

    self.assertEqual(302, response.status_int)
    self.assertEqual(f"http://localhost/_/auth/login/google?{urlencode({'redirect_to': 'http://localhost'})}",
                     response.headers['Location'])

  def test_login_endpoint__single_login_method__with_redirect_to(self):
    response = self.testapp.get('/_/auth/login?redirect_to=%2Froadmap')

    self.assertEqual(302, response.status_int)
    self.assertEqual(f"http://localhost/_/auth/login/google?{urlencode({'redirect_to': 'http://localhost/roadmap'})}",
                     response.headers['Location'])

  @patch('modules.base.handlers.LOGIN_METHODS', MULTIPLE_LOGIN_METHODS)
  def test_login_endpoint__multiple_login_methods(self):
    response = self.testapp.get('/_/auth/login')

    self.assertEqual(200, response.status_int)
    self.assertIn(f"/_/auth/login/google?{urlencode({'redirect_to': 'http://localhost'})}",
                  response.text)
    self.assertIn(f"https://mylogin/login?{urlencode({'redirect_to': 'http://localhost'})}",
                  response.text)

  @patch('modules.base.handlers.LOGIN_METHODS', MULTIPLE_LOGIN_METHODS)
  def test_login_endpoint__multiple_login_methods__with_redirect_to(self):
    response = self.testapp.get('/_/auth/login?redirect_to=%2Froadmap')

    self.assertEqual(200, response.status_int)
    self.assertIn(f"/_/auth/login/google?{urlencode({'redirect_to': 'http://localhost/roadmap'})}",
                  response.text)
    self.assertIn(f"https://mylogin/login?{urlencode({'redirect_to': 'http://localhost/roadmap'})}",
                  response.text)

  @patch('modules.base.handlers.get_config', return_value={'testing': {'secret': 'a_test_secret',
                                                                       'domains': ['example.com']}})
  def test_login_via_test_token__no_token(self, _):
    response = self.testapp.get('/_/auth/oauth2_callback')

    self.assertEqual(302, response.status_int)

  @patch('modules.base.handlers.get_config', return_value={})
  def test_login_via_test_token__no_token__no_test_token_config(self, _):
    response = self.testapp.get('/_/auth/oauth2_callback')

    self.assertEqual(302, response.status_int)

  @patch('modules.base.handlers.get_config', return_value={'testing': {'secret': 'a_test_secret',
                                                                       'domains': ['example.com']}})
  def test_login_via_test_token__invalid_token(self, _):
    token = jwt.encode({'email': 'sam@example.com'}, 'some_secret', algorithm='HS256')

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token}',
                                expect_errors=True)

    self.assertEqual(500, response.status_int)

    self._assert_authentication_status(response, False)

  @patch('modules.base.handlers.get_config', return_value={})
  def test_login_via_test_token__no_test_token_config(self, _):
    token = jwt.encode({'email': 'sam@example.com'}, 'a_test_secret', algorithm='HS256')

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token}',
                                expect_errors=True)

    self.assertEqual(500, response.status_int)

    self._assert_authentication_status(response, False)

  @patch('modules.base.handlers.get_config', return_value={'testing': {'secret': 'a_test_secret',
                                                                        'domains': ['example.com']}})
  def test_login_via_test_token__valid_token_invalid_domain(self, _):
    token = jwt.encode({'user_email': 'sam@googs.com'}, 'a_test_secret', algorithm='HS256')

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token}',
                                expect_errors=True)

    self.assertEqual(500, response.status_int)

    self._assert_authentication_status(response, False)

  @patch('modules.base.handlers.get_config', return_value={'testing': {'secret': 'a_test_secret',
                                                                        'domains': ['example.com']}})
  def test_login_via_test_token__success(self, _):
    token = jwt.encode({'user_email': 'sam@example.com'}, 'a_test_secret', algorithm='HS256')

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token}')

    self.assertEqual(302, response.status_int)

    self._assert_authentication_status(response, True, 'sam@example.com', 'example.com')


def _generate_signin_token(secret, org, expires_in_seconds, user_id=None, user_email=None, method='custom_method'):
  payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in_seconds),
             'method': method}

  if user_id:
    payload['id'] = user_id
  elif user_email:
    payload['email'] = user_email
    payload['organization'] = org
  else:
    raise ValueError('Either user_id or user_email must be provided')

  return jwt.encode(payload,
                    secret,
                    'HS256')

class TestAuthenticationControls(AuthenticationTestCase):

  def setUp(self):
    super().setUp()

    self.test_user = User(id=3,
                          created=datetime.datetime(2021, 1, 12, 1, 2, 3),
                          email='kay@googs.com',
                          domain_type='corporate',
                          organization='googs.com')
    self.test_user.put()

  def test_enabled_status__false(self):
    self.test_user.enabled = False
    self.test_user.put()

    response = self.testapp.get('/me',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual(302,
                     response.status_int)

    self.assertEqual('http://localhost/_/auth/login?e=account_disabled',
                     response.headers.get('Location'))

  def test_enabled_status__none(self):
    response = self.testapp.get('/me',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual(200,
                     response.status_int)

    self.assertEqual({'email': 'kay@googs.com',
                      'org': 'googs.com'},
                     response.json)

  def test_enabled_status__true(self):
    self.test_user.enabled = True
    self.test_user.put()

    response = self.testapp.get('/me',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual(200,
                     response.status_int)

    self.assertEqual({'email': 'kay@googs.com',
                      'org': 'googs.com'},
                     response.json)

  def _try_auth_method(self, configured_methods, try_method):
    token = _generate_signin_token('so_secret',
                                   'googs.com',
                                   30,
                                   user_email='kay@googs.com',
                                   method=try_method)

    with patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'}), \
         patch('modules.base.authentication.get_allowed_authentication_methods',
               return_value=configured_methods) as mock_get_allowed_authentication_methods:
      login_response = self.testapp.get('/_/auth/jwt?token=%s' % (token))

    mock_get_allowed_authentication_methods.assert_called_once_with('googs.com')

    return login_response

  def test_allowed_authentication_methods__none_configured(self):
    login_response = self._try_auth_method(None, 'google')

    user_info_response = self.testapp.get('/me',
                                          headers={'Cookie': login_response.headers['Set-Cookie']})

    self.assertEqual({'email': 'kay@googs.com',
                      'org': 'googs.com'},
                     user_info_response.json)

  def test_allowed_authentication_methods__configured__method_used_allowed(self):
    login_response = self._try_auth_method(['google', 'method2'], 'google')

    user_info_response = self.testapp.get('/me',
                                          headers={'Cookie': login_response.headers['Set-Cookie']})

    self.assertEqual({'email': 'kay@googs.com',
                      'org': 'googs.com'},
                     user_info_response.json)

  def test_allowed_authentication_methods__configured__method_used_not_allowed(self):
    login_response = self._try_auth_method(['method1', 'method2'], 'google')

    self._assert_authentication_status(login_response, False)

    self.assertEqual('http://localhost/_/auth/login?e=auth_not_allowed-google',
                     login_response.headers.get('Location'))


class TestJwtSignin(AuthenticationTestCase):

  def test_jwt_signin__no_token(self):
    response = self.testapp.get('/_/auth/jwt',
                                expect_errors=True)

    self.assertEqual(400, response.status_int)

    self._assert_authentication_status(response, False)

  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__malformed_token(self, _):
    response = self.testapp.get('/_/auth/jwt?token=%s' % ('nay'),
                                expect_errors=True)

    self.assertEqual(400, response.status_int)

    self._assert_authentication_status(response, False)

  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__token_signed_with_wrong_secret(self, _):
    response = self.testapp.get('/_/auth/jwt?token=%s' % (_generate_signin_token('a_secret',
                                                                                 'googs.com',
                                                                                 30,
                                                                                 user_email='jo@googs.com')),
                                expect_errors=True)

    self.assertEqual(400, response.status_int)

    self._assert_authentication_status(response, False)

  @patch('logging.warning')
  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__expired_token(self, _, mock_log_warning):
    token = _generate_signin_token('so_secret',
                                   'googs.com',
                                   -10,
                                   user_email='jo@googs.com')

    response = self.testapp.get('/_/auth/jwt?token=%s' % (token))

    self.assertEqual(302, response.status_int)

    self._assert_authentication_status(response, False)

    mock_log_warning.assert_called_once_with('Attempt to use expired JWT: %s',
                                             token)

  @patch('logging.warning')
  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__valid_token__successful_signin(self, _, mock_log_warning):
    response = self.testapp.get('/_/auth/jwt?token=%s' % (_generate_signin_token('so_secret',
                                                                                 'googs.com',
                                                                                 30,
                                                                                 user_email='jo@googs.com')))

    self.assertEqual(302, response.status_int)

    mock_log_warning.assert_not_called()

    self._assert_authentication_status(response, True, 'jo@googs.com', 'googs.com')

  @patch('logging.warning')
  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__valid_token__user_domain_not_same_as_org_domain(self, _, mock_log_warning):
    response = self.testapp.get('/_/auth/jwt?token=%s' % (_generate_signin_token('so_secret',
                                                                                 'googs.com',
                                                                                 30,
                                                                                 user_email='jo@other.com')))

    # this is still a valid login: the identity service is responsible for verifying the user is a
    # member of an org, even if a user's email domain doesn't match the org domain
    self.assertEqual(302, response.status_int)

    mock_log_warning.assert_not_called()

    self._assert_authentication_status(response, True, 'jo@other.com', 'googs.com')

  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__with_valid_redirect_to(self, _):
    token = _generate_signin_token('so_secret',
                                   'googs.com',
                                   30,
                                   user_email='jo@googs.com')

    response = self.testapp.get('/_/auth/jwt?%s' % (urlencode({'token': token,
                                                               'redirect_to': 'http://localhost/roadmap'})))

    self.assertEqual(302, response.status_int)
    self.assertEqual('http://localhost/roadmap',
                     response.headers['Location'])

    self._assert_authentication_status(response, True, 'jo@googs.com', 'googs.com')

  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__with_invalid_redirect_to(self, _):
    token = _generate_signin_token('so_secret',
                                   'googs.com',
                                   30,
                                   user_email='jo@googs.com')

    response = self.testapp.get('/_/auth/jwt?%s' % (urlencode({'token': token,
                                                               'redirect_to': 'http://localhost.net/evil'})))

    self.assertEqual(302, response.status_int)
    self.assertEqual('http://localhost',
                     response.headers['Location'])

    self._assert_authentication_status(response, True, 'jo@googs.com', 'googs.com')

  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__by_user_id__user_does_not_exist(self, _):
    response = self.testapp.get('/_/auth/jwt?token=%s' % (_generate_signin_token('so_secret',
                                                                                 'googs.com',
                                                                                 30,
                                                                                 user_id=80)),
                                expect_errors=True)

    self.assertEqual(400, response.status_int)

    self._assert_authentication_status(response, False)

  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__by_user_id__successful_signin(self, _):
    test_user = User(id=3,
                     created=datetime.datetime(2021, 1, 12, 1, 2, 3),
                     email='kay@googs.com',
                     domain_type='corporate',
                     organization='googs.com')
    test_user.put()

    login_response = self.testapp.get('/_/auth/jwt?token=%s' % (_generate_signin_token('so_secret',
                                                                                       'googs.com',
                                                                                       30,
                                                                                       user_id=3)))

    self.assertEqual(302, login_response.status_int)

    self._assert_authentication_status(login_response, True, 'kay@googs.com', 'googs.com')
