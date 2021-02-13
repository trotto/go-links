from mock import patch

from modules.data import get_models
from modules.routing import handlers
from testing import TrottoTestCase


ShortLink = get_models('links').ShortLink


class TestRedirectHandlerWithoutLogin(TrottoTestCase):

  blueprints_under_test = [handlers.routes]

  def test_get__not_logged_in__normal_redirect_from_browser_extension(self):
    response = self.testapp.get('/benefits?s=crx')

    self.assertEqual(302, response.status_int)
    self.assertEqual('http://localhost/_/auth/login?redirect_to=%2Fbenefits%3Fs%3Dcrx', response.location)

  def test_get__not_logged_in__http_bare_host_request_coming_from_browser_extension(self):
    response = self.testapp.get('/benefits?s=crx&sc=http')

    self.assertEqual(302, response.status_int)
    self.assertEqual('http://benefits?tr=ot', response.location)

  def test_get__not_logged_in__https_bare_host_request_coming_from_browser_extension(self):
    response = self.testapp.get('/benefits?s=crx&sc=https')

    self.assertEqual(302, response.status_int)
    self.assertEqual('https://benefits?tr=ot', response.location)


class TestRedirectHandler(TrottoTestCase):

  blueprints_under_test = [handlers.routes]

  def setUp(self):
    super().setUp()

    self._populate_shortlinks()

  def _populate_shortlinks(self):
    test_shortlinks = [

      ShortLink(id=321,
                organization='1.com',
                owner='jay@1.com',
                namespace='go',
                shortpath='wiki',
                shortpath_prefix='wiki',
                destination_url='http://wiki.com'),

      ShortLink(organization='1.com',
                owner='jay@1.com',
                namespace='go',
                shortpath='sfdc/%s',
                shortpath_prefix='sfdc',
                destination_url='http://sfdc.com/search/%s'),

      ShortLink(organization='1.com',
                owner='bay@1.com',
                namespace='go',
                shortpath='slack',
                shortpath_prefix='slack',
                destination_url='http://slack.com'),

      ShortLink(organization='1.com',
                owner='bay@1.com',
                namespace='eng',
                shortpath='drive',
                shortpath_prefix='drive',
                destination_url='https://eng.drive.com'),

      ShortLink(organization='2.com',
                owner='jay@2.com',
                namespace='go',
                shortpath='drive',
                shortpath_prefix='drive',
                destination_url='http://drive3.com')
    ]

    for link in test_shortlinks:
      link.put()

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

  @patch('shared_helpers.config.get_organization_config',
         side_effect=lambda org: {'namespaces': ['eng', 'prod']} if org == '1.com' else {})
  def test_redirect__logged_in__alternate_namespace__no_match(self, _):
    response = self.testapp.get('/eng/someplace',
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@1.com'})

    self.assertEqual(302, response.status_int)

    self.assertEqual('http://localhost:5007/?sp=someplace&ns=eng', response.headers['Location'])

  @patch('shared_helpers.config.get_organization_config',
         side_effect=lambda org: {'namespaces': ['eng', 'prod']} if org == '1.com' else {})
  def test_redirect__logged_in__match_for_other_namespace(self, _):
    response = self.testapp.get('/drive',
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@1.com'})

    self.assertEqual(302, response.status_int)

    self.assertEqual('http://localhost:5007/?sp=drive', response.headers['Location'])

  @patch('shared_helpers.config.get_organization_config',
         side_effect=lambda org: {'namespaces': ['eng', 'prod']} if org == '2.com' else {})
  def test_redirect__logged_in__alternate_namespace__match_in_other_org(self, _):
    response = self.testapp.get('/eng/drive',
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@2.com'})

    self.assertEqual(302, response.status_int)

    self.assertEqual('http://localhost:5007/?sp=drive&ns=eng', response.headers['Location'])

  @patch('shared_helpers.config.get_organization_config',
         side_effect=lambda org: {'namespaces': ['eng', 'prod']} if org == '1.com' else {})
  def test_redirect__logged_in__alternate_namespace__match_in_this_org(self, _):
    response = self.testapp.get('/eng/drive',
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@1.com'})

    self.assertEqual(302, response.status_int)

    self.assertEqual('https://eng.drive.com', response.headers['Location'])

  @patch('shared_helpers.config.get_organization_config',
         side_effect=lambda org: {'namespaces': ['wiki', 'prod']} if org == '1.com' else {})
  def test_redirect__logged_in__simple_go_link_matching_alternate_namespace(self, _):
    response = self.testapp.get('/wiki',
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@1.com'})

    self.assertEqual(302, response.status_int)

    self.assertEqual('http://wiki.com', response.headers['Location'])
