from mock import patch
from dataclasses import dataclass
from urllib import parse

from modules.data import get_models
from modules.routing import handlers
from modules.links import handlers as links_handlers
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

class RoutingTestCase(TrottoTestCase):
  blueprints_under_test = [handlers.routes, links_handlers.routes]

  TEST_KEYWORD = 'meeting-notes'
  TEST_DESTINATION = 'https://docs.google.com/document/d/2Bd5X-6WFpRbafPgXax98GZenmCTZkTrNxotNvb8k2vI/edit'

  def _create_test_link(self, keyword=TEST_KEYWORD, destination=TEST_DESTINATION):
    response = self.testapp.post_json('/_/api/links',
                                      {'shortpath': keyword,
                                       'destination': destination},
                                      headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertIsNotNone(response.json.get('id'))

  def _get_redirect(self, keyword):
    response = self.testapp.get('/' + keyword,
                                headers={'TROTTO_USER_UNDER_TEST': 'rex@googs.com'})

    self.assertEqual(302, response.status_int)

    return response.headers['Location']

class TestKeywordPunctuationSensitivity(RoutingTestCase):

  @patch('shared_helpers.config.get_organization_config',
         return_value={})
  def test_keyword_punctuation_sensitivity__not_specified(self, _):
    self._create_test_link()

    self.assertEqual(self.TEST_DESTINATION, self._get_redirect(self.TEST_KEYWORD))

    keyword_without_dashes = self.TEST_KEYWORD.replace('-', '')
    self.assertEqual(f'http://localhost:5007/?sp={keyword_without_dashes}', self._get_redirect(keyword_without_dashes))

  @patch('shared_helpers.config.get_organization_config',
         return_value={'keywords': {'punctuation_sensitive': False}})
  def test_keyword_punctuation_sensitivity__insensitive(self, _):
    self._create_test_link()

    self.assertEqual(self.TEST_DESTINATION, self._get_redirect(self.TEST_KEYWORD))

    keyword_without_dashes = self.TEST_KEYWORD.replace('-', '')
    self.assertEqual(self.TEST_DESTINATION, self._get_redirect(keyword_without_dashes))

    self.assertEqual(self.TEST_DESTINATION, self._get_redirect(keyword_without_dashes.upper()))

  @patch('shared_helpers.config.get_organization_config',
         return_value={'keywords': {'punctuation_sensitive': False}})
  def test_keyword_punctuation_sensitivity__insensitive__hierachical_link(self, _):
    keyword = 'meeting-notes/2022-02-11'

    self._create_test_link(keyword)

    self.assertEqual(self.TEST_DESTINATION, self._get_redirect(keyword))

    keyword_without_dashes = keyword.replace('-', '')
    self.assertEqual(self.TEST_DESTINATION, self._get_redirect(keyword_without_dashes))

  @patch('shared_helpers.config.get_organization_config',
         return_value={'keywords': {'punctuation_sensitive': False}})
  def test_keyword_punctuation_sensitivity__insensitive__programmatic_link(self, _):
    keyword = 'my-drive/quick-search/%s'
    destination = 'https://drive.google.com/drive/search?q=%s'

    self._create_test_link(keyword, destination)

    request_path = keyword.replace('%s', '2022-roadmap') # query includes punctuation
    expected_destination = destination.replace('%s', '2022-roadmap')

    self.assertEqual(expected_destination, self._get_redirect(request_path))

    request_path_without_dashes = keyword.replace('-', '').replace('%s', '2022-roadmap')
    self.assertEqual(expected_destination, self._get_redirect(request_path_without_dashes))

  @patch('shared_helpers.config.get_organization_config',
         return_value={'keywords': {'punctuation_sensitive': False}})
  def test_keyword_punctuation_sensitivity__insensitive__no_such_link(self, _):
    # autofilled link should retain punctuation
    self.assertEqual(f'http://localhost:5007/?sp={self.TEST_KEYWORD}', self._get_redirect(self.TEST_KEYWORD))


class TestAlternativeKeywordResolutionMode(RoutingTestCase):
  @dataclass
  class TestCase:
    resolution_mode: str
    requested_keyword: str
    expected_redirect: str

  def test_alternative_keyword_resolution_mode__extra_path_parts(self):
    TEST_KEYWORD = 'example'
    TEST_DESTINATION = 'https://example.com/'

    self._create_test_link(TEST_KEYWORD, TEST_DESTINATION)

    TEST_KEYWORD_WITH_EXTRA_PARTS = TEST_KEYWORD+'/extra1/extra2'

    for test_case in [
      self.TestCase(resolution_mode=None, requested_keyword=TEST_KEYWORD, expected_redirect=TEST_DESTINATION),
      self.TestCase(resolution_mode=None,
                    requested_keyword=TEST_KEYWORD_WITH_EXTRA_PARTS,
                    expected_redirect='http://localhost:5007/?'+parse.urlencode({'sp': TEST_KEYWORD_WITH_EXTRA_PARTS})),
      self.TestCase(resolution_mode='alternative', requested_keyword=TEST_KEYWORD, expected_redirect=TEST_DESTINATION),
      self.TestCase(resolution_mode='alternative',
                    requested_keyword=TEST_KEYWORD_WITH_EXTRA_PARTS,
                    expected_redirect=TEST_DESTINATION+'extra1/extra2'),
    ]:
      with patch('shared_helpers.config.get_organization_config',
                 return_value={'keywords': {'resolution_mode': test_case.resolution_mode}}):
        self.assertEqual(test_case.expected_redirect, self._get_redirect(test_case.requested_keyword))

  def test_alternative_keyword_resolution_mode__programmatic_link_without_provided_params(self):
    TEST_KEYWORD_1 = 'example/%s'
    TEST_DESTINATION_1 = 'https://example.com/?param=%s'

    TEST_KEYWORD_2 = 'example2/%s/%s'
    TEST_DESTINATION_2 = 'https://example.com/?param1=%s&param2=%s'

    self._create_test_link(TEST_KEYWORD_1, TEST_DESTINATION_1)
    self._create_test_link(TEST_KEYWORD_2, TEST_DESTINATION_2)

    TEST_KEYWORD_1_WITHOUT_PARAMS = TEST_KEYWORD_1.replace('%s', '').strip('/')
    TEST_KEYWORD_2_WITHOUT_PARAMS = TEST_KEYWORD_2.replace('%s', '').strip('/')

    for test_case in [
      self.TestCase(resolution_mode=None,
                    requested_keyword=TEST_KEYWORD_1.replace('%s', 'hello'),
                    expected_redirect=TEST_DESTINATION_1.replace('%s', 'hello')),
      self.TestCase(resolution_mode=None,
                    requested_keyword=TEST_KEYWORD_1_WITHOUT_PARAMS,
                    expected_redirect='http://localhost:5007/?'+parse.urlencode({'sp': TEST_KEYWORD_1_WITHOUT_PARAMS})),
      self.TestCase(resolution_mode='alternative',
                    requested_keyword=TEST_KEYWORD_1.replace('%s', 'hello'),
                    expected_redirect=TEST_DESTINATION_1.replace('%s', 'hello')),
      self.TestCase(resolution_mode='alternative',
                    requested_keyword=TEST_KEYWORD_1_WITHOUT_PARAMS,
                    expected_redirect=TEST_DESTINATION_1.replace('%s', '')),
      self.TestCase(resolution_mode='alternative',
                    requested_keyword=TEST_KEYWORD_2_WITHOUT_PARAMS,
                    expected_redirect=TEST_DESTINATION_2.replace('%s', '')),
    ]:
      with patch('shared_helpers.config.get_organization_config',
                 return_value={'keywords': {'resolution_mode': test_case.resolution_mode}}):
        self.assertEqual(test_case.expected_redirect, self._get_redirect(test_case.requested_keyword))
