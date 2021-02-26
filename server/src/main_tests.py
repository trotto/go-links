import os

from mock import patch
import webtest

from main import app
from modules.data import get_models
from modules.links import handlers
from shared_helpers.services import InvalidInternalToken
from testing import TrottoTestCase


ShortLink = get_models('links').ShortLink


class TestInitialization(TrottoTestCase):

  blueprints_under_test = [handlers.routes]

  def setUp(self):
    super().setUp()

    self.initial_env = os.getenv('ENVIRONMENT')

  def tearDown(self):
    super().tearDown()

    os.environ['ENVIRONMENT'] = self.initial_env

  @patch('modules.base.authentication.ADDITIONAL_ALLOWED_ORIGINS', ['mytrotto.com'])
  def test_csrf_default_enabled(self):
    testapp = webtest.TestApp(app)

    response = testapp.post_json('/_/api/links',
                                 {'shortpath': 'there',
                                  'destination': 'http://example.com/there'},
                                 headers={'origin': 'evil.com',
                                          'X-CSRFToken': 'invalidtoken',
                                          'TROTTO_USER_UNDER_TEST': 'kay@googs.com'},
                                 expect_errors=True)
    self.assertEqual(400, response.status_int)
    self.assertIn('Invalid CSRF token.', response.text)

    self.assertEqual(0, len(ShortLink._get_all()))

  @patch('modules.base.authentication.ADDITIONAL_ALLOWED_ORIGINS', ['mytrotto.com'])
  def test_csrf__no_token_but_allowed_origin(self):
    testapp = webtest.TestApp(app)

    response = testapp.post_json('/_/api/links',
                                 {'shortpath': 'there',
                                  'destination': 'http://example.com/there'},
                                 headers={'origin': 'mytrotto.com',
                                          'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})
    self.assertEqual(201, response.status_int)

  @patch('modules.base.authentication.csrf_exempt_paths', set(['/_/api/links']))
  def test_csrf__exempt_path(self):
    testapp = webtest.TestApp(app)

    response = testapp.post_json('/_/api/links',
                                 {'shortpath': 'there',
                                  'destination': 'http://example.com/there'},
                                 headers={'origin': 'mytrotto.com',
                                          'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})
    self.assertEqual(201, response.status_int)

  @patch('modules.base.authentication.validate_internal_request', side_effect=InvalidInternalToken)
  def test_csrf__invalid_internal_token(self, mock_validate_internal_request):
    testapp = webtest.TestApp(app)

    response = testapp.post_json('/_/api/links',
                                 {'shortpath': 'there',
                                  'destination': 'http://example.com/there'},
                                 headers={'origin': 'evil.com',
                                          'TROTTO_USER_UNDER_TEST': 'kay@googs.com'},
                                 expect_errors=True)
    self.assertEqual(400, response.status_int)
    self.assertIn('Invalid CSRF token.', response.text)

    self.assertEqual(0, len(ShortLink._get_all()))

    mock_validate_internal_request.assert_called_once()

  @patch('modules.base.authentication.validate_internal_request', return_value=True)
  def test_csrf__valid_internal_token(self, mock_validate_internal_request):
    testapp = webtest.TestApp(app)

    response = testapp.post_json('/_/api/links',
                                 {'shortpath': 'there',
                                  'destination': 'http://example.com/there'},
                                 headers={'origin': 'mytrotto.com',
                                          'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})
    self.assertEqual(201, response.status_int)

    mock_validate_internal_request.assert_called_once()

  def test_user_under_test_does_not_work_by_default(self):
    del os.environ['ENVIRONMENT']

    self.init_app()

    response = self.testapp.post_json('/_/api/links',
                                      {'shortpath': 'there',
                                       'destination': 'http://example.com/there'},
                                      headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'},
                                      expect_errors=True)

    self.assertEqual(401, response.status_int)

    os.environ['ENVIRONMENT'] = self.initial_env

    self.assertEqual(0, len(ShortLink._get_all()))
