import datetime
import os
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from freezegun import freeze_time
import webtest
from webapp2_extras import securecookie

from modules.base.handlers import get_secrets
from modules.links.models import ShortLink
from modules.routing import handlers

class TestRedirectHandlerWithoutLogin(unittest.TestCase):

  def _set_up_gae_testbed(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()

    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    self.testbed.init_taskqueue_stub(root_path=os.path.join(os.path.dirname(__file__), '../../..'))

  def setUp(self):
    self._set_up_gae_testbed()

    # see https://cloud.google.com/appengine/docs/standard/python/tools/handlertesting
    self.testapp = webtest.TestApp(handlers.app)

  def get_cookie_for_session(self, session_object):
    sessions_secret = get_secrets().get('sessions_secret')
    serializer = securecookie.SecureCookieSerializer(sessions_secret)

    return serializer.serialize('session', {'_sid': session_object.key.id()})

  def tearDown(self):
    self.testbed.deactivate()

  def test_get__not_logged_in__normal_redirect_from_chrome_extension(self):
    response = self.testapp.get('/benefits?s=crx')

    self.assertEqual(200, response.status_int)
    self.assertIn('src="/_images/auth/google_signin_button.png"', response.body)

  def test_get__not_logged_in__http_bare_host_request_coming_from_chrome_extension(self):
    response = self.testapp.get('/benefits?s=crx&sc=http')

    self.assertEqual(302, response.status_int)
    self.assertEqual('http://benefits?tr=ot', response.location)

  def test_get__not_logged_in__https_bare_host_request_coming_from_chrome_extension(self):
    response = self.testapp.get('/benefits?s=crx&sc=https')

    self.assertEqual(302, response.status_int)
    self.assertEqual('https://benefits?tr=ot', response.location)


class TestRedirectHandler(unittest.TestCase):
  def _set_up_gae_testbed(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()

    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    self.testbed.init_taskqueue_stub(root_path=os.path.join(os.path.dirname(__file__), '../../..'))

  def setUp(self):
    self._set_up_gae_testbed()

    # see https://cloud.google.com/appengine/docs/standard/python/tools/handlertesting
    self.testapp = webtest.TestApp(handlers.app)

    self._populate_shortlinks()

  def _populate_shortlinks(self):
    test_shortlinks = [

      ShortLink(id=321,
                organization='1.com',
                owner='jay@1.com',
                shortpath='wiki',
                shortpath_prefix='wiki',
                destination_url='http://wiki.com'),

      ShortLink(organization='1.com',
                owner='jay@1.com',
                shortpath='sfdc/%s',
                shortpath_prefix='sfdc',
                destination_url='http://sfdc.com/search/%s'),

      ShortLink(organization='1.com',
                owner='bay@1.com',
                shortpath='slack',
                shortpath_prefix='slack',
                destination_url='http://slack.com'),


      ShortLink(organization='2.com',
                owner='jay@2.com',
                shortpath='drive',
                shortpath_prefix='drive',
                destination_url='http://drive3.com')
    ]

    ndb.put_multi(test_shortlinks)

  def test_redirect__logged_in__go_link_does_not_exist(self):
    response = self.testapp.get('/drive',
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@1.com'})

    self.assertEqual(302, response.status_int)

    self.assertEqual('http://localhost:5007/?sp=drive', response.headers['Location'])

  def test_redirect__logged_in__simple_go_link(self):
    response = self.testapp.get('/wiki',
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@1.com'})

    self.assertEqual(302, response.status_int)

    self.assertEqual('http://wiki.com', response.headers['Location'])

  @freeze_time("2018-10-31")
  def test_redirect__logged_in__simple_go_link__using_extension(self):
    response = self.testapp.get('/wiki?s=crx',
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@1.com'})

    self.assertEqual(302, response.status_int)

    self.assertEqual('http://wiki.com', response.headers['Location'])

  def test_redirect__logged_in__go_link_with_pattern(self):
    response = self.testapp.get('/sfdc/micro',
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@1.com'})

    self.assertEqual(302, response.status_int)

    self.assertEqual('http://sfdc.com/search/micro', response.headers['Location'])

  def test_redirect__logged_in__uppercase_keyword(self):
    response = self.testapp.get('/WIKI',
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@1.com'})

    self.assertEqual(302, response.status_int)

    self.assertEqual('http://wiki.com', response.headers['Location'])

  def test_redirect__logged_in__pattern_with_uppercase_keyword_and_search_term(self):
    response = self.testapp.get('/SFdc/Micro',
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@1.com'})

    self.assertEqual(302, response.status_int)

    self.assertEqual('http://sfdc.com/search/Micro', response.headers['Location'])
