import datetime
from urllib.parse import urlencode

import jwt
from mock import patch

from modules.base import handlers
from testing import TrottoTestCase


class TestHandlers(TrottoTestCase):

  blueprints_under_test = [handlers.routes]

  def test_login_endpoint__no_upstream_host_header(self):
    response = self.testapp.get('/_/auth/login',
                                headers={'Host': 'trot.to'})

    expected_oauth_redirect_uri = urlencode({'redirect_uri': 'https://trot.to/_/auth/oauth2_callback'})

    self.assertEqual(302, response.status_int)
    self.assertIn(expected_oauth_redirect_uri, response.headers['Location'])

  def test_login_endpoint__upstream_host_header(self):
    response = self.testapp.get('/_/auth/login',
                                headers={'Host': 'trot.to',
                                         'X-Upstream-Host': 'go.trot.to'})

    expected_oauth_redirect_uri = urlencode({'redirect_uri': 'https://go.trot.to/_/auth/oauth2_callback'})

    self.assertEqual(302, response.status_int)
    self.assertIn(expected_oauth_redirect_uri, response.headers['Location'])

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

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token.decode("utf-8")}',
                                expect_errors=True)

    self.assertEqual(500, response.status_int)
    self.assertEqual(None, response.headers.get('Set-Cookie'))

  @patch('modules.base.handlers.get_config', return_value={})
  def test_login_via_test_token__no_test_token_config(self, _):
    token = jwt.encode({'email': 'sam@example.com'}, 'a_test_secret', algorithm='HS256')

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token.decode("utf-8")}',
                                expect_errors=True)

    self.assertEqual(500, response.status_int)
    self.assertEqual(None, response.headers.get('Set-Cookie'))

  @patch('modules.base.handlers.get_config', return_value={'testing': {'secret': 'a_test_secret',
                                                                        'domains': ['example.com']}})
  def test_login_via_test_token__valid_token_invalid_domain(self, _):
    token = jwt.encode({'user_email': 'sam@googs.com'}, 'a_test_secret', algorithm='HS256')

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token.decode("utf-8")}',
                                expect_errors=True)

    self.assertEqual(500, response.status_int)
    self.assertEqual(None, response.headers.get('Set-Cookie'))

  @patch('modules.base.handlers.get_config', return_value={'testing': {'secret': 'a_test_secret',
                                                                        'domains': ['example.com']}})
  def test_login_via_test_token__success(self, _):
    token = jwt.encode({'user_email': 'sam@example.com'}, 'a_test_secret', algorithm='HS256')

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token.decode("utf-8")}')

    self.assertEqual(302, response.status_int)
    self.assertEqual(True, response.headers.get('Set-Cookie').startswith('session='))


class TestJwtSignin(TrottoTestCase):

  blueprints_under_test = [handlers.routes]

  def _generate_token(self, secret, email, org, expires_in_seconds):
    return jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in_seconds),
                       'email': email,
                       'organization': org},
                      secret,
                      'HS256').decode('utf-8')

  def test_jwt_signin__no_token(self):
    response = self.testapp.get('/_/auth/jwt',
                                expect_errors=True)

    self.assertEqual(400, response.status_int)

    self.assertNotIn('session=', response.headers.get('Set-Cookie', ''))

  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__malformed_token(self, _):
    response = self.testapp.get('/_/auth/jwt?token=%s' % ('nay'),
                                expect_errors=True)

    self.assertEqual(400, response.status_int)

    self.assertNotIn('session=', response.headers.get('Set-Cookie', ''))

  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__token_signed_with_wrong_secret(self, _):
    response = self.testapp.get('/_/auth/jwt?token=%s' % (self._generate_token('a_secret',
                                                                               'jo@googs.com',
                                                                               'googs.com',
                                                                               30)),
                                expect_errors=True)

    self.assertEqual(400, response.status_int)

    self.assertNotIn('session=', response.headers.get('Set-Cookie', ''))

  @patch('logging.warning')
  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__expired_token(self, _, mock_log_warning):
    token = self._generate_token('so_secret',
                                 'jo@googs.com',
                                 'googs.com',
                                 -10)

    response = self.testapp.get('/_/auth/jwt?token=%s' % (token))

    self.assertEqual(302, response.status_int)

    self.assertNotIn('session=', response.headers.get('Set-Cookie', ''))

    mock_log_warning.assert_called_once_with('Attempt to use expired JWT: %s',
                                             token)

  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__valid_token__mismatched_org(self, _):
    response = self.testapp.get('/_/auth/jwt?token=%s' % (self._generate_token('so_secret',
                                                                               'jo@googs.com',
                                                                               'other.com',
                                                                               30)),
                                expect_errors=True)

    self.assertEqual(400, response.status_int)

    self.assertNotIn('session=', response.headers.get('Set-Cookie', ''))

  @patch('logging.warning')
  @patch('modules.base.handlers.get_config', return_value={'sessions_secret': 'so_secret'})
  def test_jwt_signin__valid_token__successful_signin(self, _, mock_log_warning):
    response = self.testapp.get('/_/auth/jwt?token=%s' % (self._generate_token('so_secret',
                                                                               'jo@googs.com',
                                                                               'googs.com',
                                                                               30)))

    self.assertEqual(302, response.status_int)

    mock_log_warning.assert_not_called()

    self.assertIn('session=', response.headers.get('Set-Cookie', ''))
