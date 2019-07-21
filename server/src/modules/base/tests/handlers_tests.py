import json
import os

import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from mock import patch, Mock
import webapp2
from webapp2_extras.appengine import sessions_ndb
import webtest

from modules.base import authentication
from modules.base import handlers
from modules.links import handlers as links_handlers
from modules.links.models import ShortLink
from modules.users.models import User

class TestHandlers(unittest.TestCase):

  def _set_up_gae_testbed(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()

    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    self.testbed.init_taskqueue_stub(root_path=os.path.join(os.path.dirname(__file__), '../../..'))

  def setUp(self):
    self._set_up_gae_testbed()

    self.testapp = webtest.TestApp(handlers.app)

  def tearDown(self):
    self.testbed.deactivate()

  @patch.object(handlers.BaseHandler, 'attempt_auth_by_user_header')
  @patch('shared_helpers.env.current_env_is_local', return_value=True)
  def test_login_via_user_header__is_local(self, mock_current_env_is_production, mock_attempt_auth_by_user_header):
    self.testapp.get('/_/auth/logout')

    self.assertTrue(mock_current_env_is_production.called)
    self.assertTrue(mock_attempt_auth_by_user_header.called)

  @patch.object(handlers.BaseHandler, 'attempt_auth_by_user_header')
  @patch('shared_helpers.env.current_env_is_local', return_value=False)
  def test_login_via_user_header__is_not_local(self, mock_current_env_is_local, mock_attempt_auth_by_user_header):
    self.testapp.get('/_/auth/logout')

    self.assertTrue(mock_current_env_is_local.called)
    self.assertFalse(mock_attempt_auth_by_user_header.called)

  def test_authentication__no_auth_provided(self):
    testapp = webtest.TestApp(links_handlers.app)

    response = testapp.get('/_/api/links')

    self.assertIn('redirect_to', json.loads(response.body))
