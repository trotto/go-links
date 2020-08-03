import jwt
from urllib.parse import urlencode

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

  @patch('modules.base.handlers.get_secrets', return_value={'testing': {'secret': 'a_test_secret',
                                                                        'domains': ['example.com']}})
  def test_login_via_test_token__no_token(self, _):
    response = self.testapp.get('/_/auth/oauth2_callback')

    self.assertEqual(302, response.status_int)

  @patch('modules.base.handlers.get_secrets', return_value={})
  def test_login_via_test_token__no_token__no_test_token_config(self, _):
    response = self.testapp.get('/_/auth/oauth2_callback')

    self.assertEqual(302, response.status_int)

  @patch('modules.base.handlers.get_secrets', return_value={'testing': {'secret': 'a_test_secret',
                                                                        'domains': ['example.com']}})
  def test_login_via_test_token__invalid_token(self, _):
    token = jwt.encode({'email': 'sam@example.com'}, 'some_secret', algorithm='HS256')

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token.decode("utf-8")}',
                                expect_errors=True)

    self.assertEqual(500, response.status_int)
    self.assertEqual(None, response.headers.get('Set-Cookie'))

  @patch('modules.base.handlers.get_secrets', return_value={})
  def test_login_via_test_token__no_test_token_config(self, _):
    token = jwt.encode({'email': 'sam@example.com'}, 'a_test_secret', algorithm='HS256')

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token.decode("utf-8")}',
                                expect_errors=True)

    self.assertEqual(500, response.status_int)
    self.assertEqual(None, response.headers.get('Set-Cookie'))

  @patch('modules.base.handlers.get_secrets', return_value={'testing': {'secret': 'a_test_secret',
                                                                        'domains': ['example.com']}})
  def test_login_via_test_token__valid_token_invalid_domain(self, _):
    token = jwt.encode({'user_email': 'sam@googs.com'}, 'a_test_secret', algorithm='HS256')

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token.decode("utf-8")}',
                                expect_errors=True)

    self.assertEqual(500, response.status_int)
    self.assertEqual(None, response.headers.get('Set-Cookie'))

  @patch('modules.base.handlers.get_secrets', return_value={'testing': {'secret': 'a_test_secret',
                                                                        'domains': ['example.com']}})
  def test_login_via_test_token__success(self, _):
    token = jwt.encode({'user_email': 'sam@example.com'}, 'a_test_secret', algorithm='HS256')

    response = self.testapp.get(f'/_/auth/oauth2_callback?test_token={token.decode("utf-8")}')

    self.assertEqual(302, response.status_int)
    self.assertEqual(True, response.headers.get('Set-Cookie').startswith('session='))
