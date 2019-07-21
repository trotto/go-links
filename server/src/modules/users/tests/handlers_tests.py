import json
import unittest

from google.appengine.ext import testbed

import webtest

from modules.users.models import User
from modules.users import handlers

class TestUserHandlers(unittest.TestCase):

  def _set_up_gae_testbed(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()

    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    self.testbed.init_taskqueue_stub()

  def setUp(self):
    self._set_up_gae_testbed()

    self.testapp = webtest.TestApp(handlers.app)

  def tearDown(self):
    self.testbed.deactivate()

  def test_user_info_endpoint(self):
    User(id=777,
         email='kay@googs.com',
         domain_type='corporate').put()

    User(id=8675,
         email='ray@googs.com',
         domain_type='corporate').put()

    response = self.testapp.get('/_/api/users/me',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual(json.loads(response.text),
                     {'email': 'kay@googs.com',
                      'role': None,
                      'admin': False,
                      'notifications': {}})

    response = self.testapp.get('/_/api/users/me',
                                headers={'TROTTO_USER_UNDER_TEST': 'ray@googs.com'})

    self.assertEqual(json.loads(response.text),
                     {'email': 'ray@googs.com',
                      'role': None,
                      'admin': False,
                      'notifications': {}})
