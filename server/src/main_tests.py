import os

import webtest

from main import app
from modules.data import get_models
from modules.links import handlers
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

  def test_csrf_default_enabled(self):
    testapp = webtest.TestApp(app)

    response = testapp.post_json('/_/api/links',
                                 {'shortpath': 'there',
                                  'destination': 'http://example.com/there'},
                                 headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'},
                                 expect_errors=True)
    self.assertEqual(400, response.status_int)
    self.assertIn('The CSRF token is missing.', response.text)

    self.assertEqual(0, len(ShortLink._get_all()))

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
