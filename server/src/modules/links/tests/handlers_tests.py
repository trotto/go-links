from typing import Optional, Type
import base64
from copy import deepcopy
from dataclasses import dataclass
import datetime
import json
from typing import List

from freezegun import freeze_time
import jwt
from mock import patch, call

from modules.data import get_models
from modules.data.abstract import api_tokens, links, users
from modules.links import handlers
from shared_helpers.utils import generate_secret
from testing import TrottoTestCase

ShortLink: Type[links.ShortLink] = get_models('links').ShortLink
User: Type[users.User] = get_models('users').User
ApiToken: Type[api_tokens.ApiToken] = get_models('api_tokens').ApiToken


class TestHandlers(TrottoTestCase):
  blueprints_under_test = [handlers.routes]

  @patch('modules.links.helpers.create_short_link')
  def test_create_link(self, mock_create_short_link):
    mock_shortlink = ShortLink(id=123,
                               created=datetime.datetime(2018, 10, 1),
                               modified=datetime.datetime(2018, 11, 1),
                               organization='googs.com',
                               owner='kay@googs.com',
                               namespace='go',
                               shortpath='there',
                               shortpath_prefix='there',
                               destination_url='http://example.com/there')

    # get a deepcopy of the args since `current_user` will be None by the time we assert
    args_deep_copy = None
    def side_effect(*args):
      nonlocal args_deep_copy
      args_deep_copy = deepcopy(args)
      return mock_shortlink

    mock_create_short_link.side_effect = side_effect

    response = self.testapp.post_json('/_/api/links',
                                      {'shortpath': 'there',
                                       'destination': 'http://example.com/there'},
                                      headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual({'id': '123',
                      'created': '2018-10-01 00:00:00',
                      'modified': '2018-11-01 00:00:00',
                      'owner': 'kay@googs.com',
                      'namespace': 'go',
                      'shortpath': 'there',
                      'destination_url': 'http://example.com/there',
                      'type': None,
                      'visits_count': 0},
                     json.loads(response.text))

    self.assertEqual(list(args_deep_copy),
                     [User.get_by_email_and_org('kay@googs.com', 'googs.com'), 'googs.com', 'kay@googs.com', 'go', 'there', 'http://example.com/there', 'simple'])

  def test_create_link__no_patching__no_namespace_specified(self):
    self.testapp.post_json('/_/api/links',
                           {'shortpath': 'favorites',
                            'destination': 'http://example.com'},
                           headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    shortlinks = ShortLink._get_all()

    self.assertEqual(1, len(shortlinks))

    shortlink = shortlinks[0]

    self.assertEqual(None, shortlink._ns)  # namespace of "go" is null in the database
    self.assertEqual('favorites', shortlink.shortpath)
    self.assertEqual('http://example.com', shortlink.destination_url)

  def test_create_link__no_patching__go_namespace_specified(self):
    self.testapp.post_json('/_/api/links',
                           {'namespace': 'go',
                            'shortpath': 'favorites',
                            'destination': 'http://example.com'},
                           headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    shortlinks = ShortLink._get_all()

    self.assertEqual(1, len(shortlinks))

    shortlink = shortlinks[0]

    self.assertEqual(None, shortlink._ns)  # namespace of "go" is null in the database
    self.assertEqual('favorites', shortlink.shortpath)
    self.assertEqual('http://example.com', shortlink.destination_url)

  @patch('shared_helpers.config.get_organization_config',
         side_effect=lambda org: {'namespaces': ['eng', 'prod']} if org == 'googs.com' else {})
  def test_create_link__config_patching_only__other_namespace_specified(self, _):
    self.testapp.post_json('/_/api/links',
                           {'namespace': 'eng',
                            'shortpath': 'favorites',
                            'destination': 'http://example.com'},
                           headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    shortlinks = ShortLink._get_all()

    self.assertEqual(1, len(shortlinks))

    shortlink = shortlinks[0]

    self.assertEqual('eng', shortlink._ns)
    self.assertEqual('favorites', shortlink.shortpath)
    self.assertEqual('http://example.com', shortlink.destination_url)

  def test_create_link__owner_specified__current_user_is_not_admin(self):
    response = self.testapp.post_json('/_/api/links',
                                      {'shortpath': 'there',
                                       'destination': 'http://example.com/there',
                                       'owner': 'joe@googs.com'},
                                      headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'},
                                      expect_errors=True)

    self.assertEqual(403, response.status_int)

    self.assertEqual(0, len(ShortLink._get_all()))

  @patch('modules.users.helpers.is_user_admin', side_effect=lambda user: user.email == 'kay@googs.com')
  def test_create_link__owner_specified__current_user_is_admin(self, _):
    response = self.testapp.post_json('/_/api/links',
                                      {'shortpath': 'there',
                                       'destination': 'http://example.com/there',
                                       'owner': 'joe@googs.com'},
                                      headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual(201, response.status_int)

    self.assertEqual('joe@googs.com', response.json['owner'])

  def test_create_link__multipart_keyword(self):
    @dataclass
    class TestCase:
      resolution_mode: str
      keywords: List[str]
      expected_error_string: str

    for test_case in [
      TestCase(resolution_mode=None, keywords=['example', 'example/%s'], expected_error_string=None),
      TestCase(resolution_mode=None, keywords=['example', 'example/part2'], expected_error_string=None),
      TestCase(resolution_mode='alternative',
               keywords=['example', 'example/%s'],
               expected_error_string='A conflicting go link already exists'),
      TestCase(resolution_mode='alternative',
               keywords=['example', 'example/part2'],
               expected_error_string='Only "%s" placeholders'),
    ]:
      self.tearDown()
      self.setUp()

      with patch('shared_helpers.config.get_organization_config',
                 return_value={'keywords': {'resolution_mode': test_case.resolution_mode}}):
        response = None
        for keyword in test_case.keywords:
          response = self.testapp.post_json('/_/api/links',
                                            {'shortpath': keyword,
                                             'destination': 'http://example.com/'+keyword},
                                            headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

        if test_case.expected_error_string:
          self.assertIn(test_case.expected_error_string, response.json.get('error'))
        else:
          self.assertEqual(None, response.json.get('error'))

  def test_get_shortlinks_for_user(self):
    modified_datetime = datetime.datetime.utcnow() + datetime.timedelta(days=2)

    with freeze_time(modified_datetime):
      ShortLink(id=1,
                created=datetime.datetime(2018, 10, 1),
                organization='googs.com',
                owner='kay@googs.com',
                namespace='go',
                shortpath='there',
                shortpath_prefix='there',
                destination_url='http://example.com'
                ).put()
      ShortLink(id=2,
                created=datetime.datetime(2018, 11, 1),
                organization='googs.com',
                owner='jay@googs.com',
                # no namespace explicitly set,
                shortpath='here',
                shortpath_prefix='here',
                destination_url='http://gmail.com'
                ).put()
      ShortLink(id=3,
                organization='widgets.com',
                owner='el@widgets.com',
                namespace='go',
                shortpath='elsewhere',
                shortpath_prefix='elsewhere',
                destination_url='http://drive.com'
                ).put()
      ShortLink(id=4,
                created=datetime.datetime(2019, 11, 1),
                organization='googs.com',
                owner='jay@googs.com',
                namespace='eng',
                shortpath='1',
                shortpath_prefix='1',
                destination_url='http://1.com').put()
      ShortLink(id=5,
                organization='widgets.com',
                owner='el@widgets.com',
                namespace='eng',
                shortpath='2',
                shortpath_prefix='2',
                destination_url='http://2.com').put()

    response = self.testapp.get('/_/api/links',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertCountEqual([{'id': '1',
                            'created': '2018-10-01 00:00:00',
                            'modified': str(modified_datetime),
                            'mine': True,
                            'owner': 'kay@googs.com',
                            'namespace': 'go',
                            'shortpath': 'there',
                            'destination_url': 'http://example.com',
                            'type': None,
                            'visits_count': 0},
                           {'id': '2',
                            'created': '2018-11-01 00:00:00',
                            'modified': str(modified_datetime),
                            'mine': False,
                            'owner': 'jay@googs.com',
                            'namespace': 'go',
                            'shortpath': 'here',
                            'destination_url': 'http://gmail.com',
                            'type': None,
                            'visits_count': 0},
                           {'id': '4',
                            'created': '2019-11-01 00:00:00',
                            'modified': str(modified_datetime),
                            'mine': False,
                            'owner': 'jay@googs.com',
                            'namespace': 'eng',
                            'shortpath': '1',
                            'destination_url': 'http://1.com',
                            'type': None,
                            'visits_count': 0}],
                          json.loads(response.text))

  def test_get_links_with_similar_to_and_limit(self):
    modified_datetime = datetime.datetime.utcnow() + datetime.timedelta(days=2)

    with freeze_time(modified_datetime):
      def _put_shortlink_into_db(pk:int, shortpath: str) -> ShortLink:
        return ShortLink(
          id=pk,
          created=datetime.datetime(2018, 10, 1),
          organization='googs.com',
          owner='kay@googs.com',
          namespace='go',
          shortpath=shortpath,
          shortpath_prefix='there',
          destination_url='http://example.com',
        ).put()

      def _get_shortlink_by_shortpath(pk:int, shortpath: str):
        return {
          'id': str(pk),
          'created': '2018-10-01 00:00:00',
          'modified': str(modified_datetime),
          'mine': True,
          'owner': 'kay@googs.com',
          'namespace': 'go',
          'shortpath': shortpath,
          'destination_url': 'http://example.com',
          'type': None,
          'visits_count': 0,
        }

      shrotpath_list: list[tuple[int, str]] = [
        (1, 'maproad'),
        (2, 'roadmap'),
        (3, 'roadmap2022'),
        (4, 'roadcrap'),
        (5, 'noize'),
        (6, 'noize2'),
        (7, 'roadmap-2023'),
        (8, '1984-map'),
        *[(index, f'noize_to_check_a_big_difference_{index}') for index in range(9, 1001)], 
      ]

      # generating 1k links
      for pk, shortpath in shrotpath_list:
        _put_shortlink_into_db(pk, shortpath)

    test_params = [{
      # checking regular option
      'shortpath_to_test': 'roadmpa',
      'limit': 5,
      'similarity_threshold': 0.5,
      'expected_list': [
        (2, 'roadmap'),
        (4, 'roadcrap'),
        (3, 'roadmap2022'),
        (7, 'roadmap-2023'),
      ]
    }, {
      # do not path similarity_trheshold
      'shortpath_to_test': 'roadmpa',
      'limit': 6,
      'expected_list': [
        (2, 'roadmap'),
        (4, 'roadcrap'),
        (3, 'roadmap2022'),
        (1, 'maproad'),
        (7, 'roadmap-2023'),
        (8, '1984-map'),
      ]
    }, {
      # without limit
      'shortpath_to_test': 'roadmpa',
      'similarity_threshold': 0.86,
      'expected_list': [
        (2, 'roadmap'),
        (4, 'roadcrap'),
        (3, 'roadmap2022'),
        (1, 'maproad'),
        (7, 'roadmap-2023'),
      ]
    }]
    
    for params in test_params:
      unexisting_shortpath = params.get('shortpath_to_test')
      limit = params.get('limit')
      similarity_threshold = params.get('similarity_threshold')
      expected_list = params.get('expected_list')

      start_time = datetime.datetime.utcnow()
      url = f'/_/api/links?similar_to={unexisting_shortpath}'
      if limit:
        url += f'&limit={limit}'
      if similarity_threshold:
        url += f'&similarity_threshold={similarity_threshold}'
      response = self.testapp.get(url,
                                  headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})
      execution_time = datetime.datetime.utcnow() - start_time
      self.assertLess(execution_time, datetime.timedelta(seconds=0.5))

      actual_response = json.loads(response.text)
      expected_response = [_get_shortlink_by_shortpath(pk, shortpath)
                          for pk, shortpath in expected_list]

      print([res['shortpath'] for res in actual_response])

      self.assertCountEqual(expected_response, actual_response)


  def test_update_link__go_link__successful(self):
    ShortLink(id=7,
              organization='googs.com',
              owner='kay@googs.com',
              namespace='go',
              shortpath='there',
              shortpath_prefix='there',
              destination_url='http://example.com'
              ).put()

    self.testapp.put_json('/_/api/links/7',
                          {'destination': 'http://boop.com'},
                          headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    shortlink = ShortLink.get_by_id(7)

    self.assertEqual('http://boop.com', shortlink.destination_url)

  def test_create_update_link__validation_override(self):
    response = self.testapp.post_json('/_/api/links?validation=expanded',
                                      {'shortpath': 'こんにちは',
                                       'destination': 'https://www.trot.to'},
                                      headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    new_link_id = response.json.get('id')
    self.assertIsNotNone(new_link_id)
    shortlink = ShortLink.get_by_id(new_link_id)

    self.assertEqual('https://www.trot.to', shortlink.destination_url)

    self.testapp.put_json(f'/_/api/links/{new_link_id}',
                          {'destination': 'https://github.com/trotto'},
                          headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    shortlink = ShortLink.get_by_id(new_link_id)

    self.assertEqual('https://github.com/trotto', shortlink.destination_url)


  def test_created_and_modified_date_tracking(self):
    time_1 = datetime.datetime.utcnow() + datetime.timedelta(days=2)
    time_2 = time_1 + datetime.timedelta(days=2)

    with freeze_time(time_1):
      self.testapp.post_json('/_/api/links',
                             {'shortpath': 'boop',
                              'destination': 'http://example.com'},
                             headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    response = self.testapp.get('/_/api/links',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    link = json.loads(response.text)[0]

    self.assertEqual(str(time_1), link['created'])
    self.assertEqual(str(time_1), link['modified'])

    with freeze_time(time_2):
      self.testapp.put_json('/_/api/links/%s' % (link['id']),
                            {'destination': 'http://example.com/path'},
                            headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    response = self.testapp.get('/_/api/links',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    link = json.loads(response.text)[0]

    self.assertEqual(str(time_1), link['created'])
    self.assertEqual(str(time_2), link['modified'])

  def test_update_link__go_link_of_other_user__current_user_is_not_admin(self):
    ShortLink(id=7,
              organization='googs.com',
              owner='kay@googs.com',
              namespace='go',
              shortpath='there',
              shortpath_prefix='there',
              destination_url='http://drive.com'
              ).put()

    response = self.testapp.put_json('/_/api/links/7',
                                     {'destination': 'http://boop.com'},
                                     headers={'TROTTO_USER_UNDER_TEST': 'rex@googs.com'},
                                     expect_errors=True)

    self.assertEqual(403, response.status_int)

    shortlink = ShortLink.get_by_id(7)

    self.assertEqual('http://drive.com', shortlink.destination_url)

  @patch('modules.users.helpers.is_user_admin', side_effect=lambda user: user.email == 'rex@googs.com')
  def test_update_link__go_link_of_other_user__current_user_is_admin(self, mock_is_user_admin):
    ShortLink(id=7,
              organization='googs.com',
              owner='kay@googs.com',
              namespace='go',
              shortpath='there',
              shortpath_prefix='there',
              destination_url='http://drive.com'
              ).put()

    self.testapp.put_json('/_/api/links/7',
                          {'destination': 'http://boop.com'},
                          headers={'TROTTO_USER_UNDER_TEST': 'rex@googs.com'})

    shortlink = ShortLink.get_by_id(7)

    self.assertEqual('http://boop.com', shortlink.destination_url)

    self.assertEqual(1, mock_is_user_admin.call_count)

  @patch('modules.links.handlers.get_org_edit_mode', return_value='any_org_user')
  def test_update_link__go_link_of_other_user__current_user_not_admin__open_edit_mode(self, _):
    ShortLink(id=7,
              organization='googs.com',
              owner='kay@googs.com',
              namespace='go',
              shortpath='there',
              shortpath_prefix='there',
              destination_url='http://drive.com'
              ).put()

    response = self.testapp.put_json('/_/api/links/7',
                                     {'destination': 'http://boop.com'},
                                     headers={'TROTTO_USER_UNDER_TEST': 'rex@googs.com'})

    self.assertEqual(200, response.status_int)

    shortlink = ShortLink.get_by_id(7)

    self.assertEqual('http://boop.com', shortlink.destination_url)

    # user still shouldn't be able to delete the go link
    response = self.testapp.delete('/_/api/links/7',
                                   headers={'TROTTO_USER_UNDER_TEST': 'rex@googs.com'},
                                   expect_errors=True)

    self.assertEqual(403, response.status_int)

    shortlink = ShortLink.get_by_id(7)

    self.assertIsNotNone(shortlink)

  @patch('modules.users.helpers.is_user_admin', return_value=True)
  def test_update_link__go_link_of_other_user__current_user_is_admin_for_different_org(self, mock_is_user_admin):
    ShortLink(id=7,
              organization='widgets.com',
              owner='kc@widgets.com',
              namespace='go',
              shortpath='there',
              shortpath_prefix='there',
              destination_url='http://drive.com'
              ).put()

    response = self.testapp.put_json('/_/api/links/7',
                                     {'destination': 'http://boop.com'},
                                     headers={'TROTTO_USER_UNDER_TEST': 'rex@googs.com'},
                                     expect_errors=True)

    self.assertEqual(403, response.status_int)

    shortlink = ShortLink.get_by_id(7)

    self.assertEqual('http://drive.com', shortlink.destination_url)

  def test_update_link__go_link_of_other_company(self):
    ShortLink(id=7,
              organization='googs.com',
              owner='kay@googs.com',
              namespace='go',
              shortpath='there',
              shortpath_prefix='there',
              destination_url='http://drive.com'
              ).put()

    response = self.testapp.put_json('/_/api/links/7',
                                     {'destination': 'http://boop.com'},
                                     headers={'TROTTO_USER_UNDER_TEST': 'kay@micro.com'},
                                     expect_errors=True)

    self.assertEqual(403, response.status_int)

    shortlink = ShortLink.get_by_id(7)

    self.assertEqual('http://drive.com', shortlink.destination_url)

  @patch('shared_helpers.events.enqueue_event')
  def test_delete_link__not_authorized(self, mock_enqueue_event):
    ShortLink(id=7,
              organization='googs.com',
              owner='kay@googs.com',
              namespace='go',
              shortpath='there',
              shortpath_prefix='there',
              destination_url='http://drive.com'
              ).put()

    response = self.testapp.delete('/_/api/links/7',
                                   headers={'TROTTO_USER_UNDER_TEST': 'jay@googs.com'},
                                   expect_errors=True)

    self.assertEqual(403, response.status_int)

    shortlink = ShortLink.get_by_id(7)

    self.assertIsNotNone(shortlink)

    mock_enqueue_event.assert_not_called()

  @patch('shared_helpers.events.enqueue_event')
  def test_delete_link__link_does_not_exist(self, mock_enqueue_event):
    ShortLink(id=7,
              organization='googs.com',
              owner='kay@googs.com',
              namespace='go',
              shortpath='there',
              shortpath_prefix='there',
              destination_url='http://drive.com'
              ).put()

    response = self.testapp.delete('/_/api/links/8',
                                   headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'},
                                   expect_errors=True)

    self.assertEqual(403, response.status_int)

    mock_enqueue_event.assert_not_called()

  @patch('modules.links.handlers.enqueue_event')
  def test_delete_link__success(self, mock_enqueue_event):
    test_shortlink = ShortLink(id=7,
                               organization='googs.com',
                               owner='kay@googs.com',
                               namespace='go',
                               shortpath='there',
                               shortpath_prefix='there',
                               destination_url='http://drive.com')
    test_shortlink.put()

    response = self.testapp.delete('/_/api/links/7',
                                   headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual(200, response.status_int)
    self.assertEqual('{}\n', response.text)

    shortlink = ShortLink.get_by_id(7)

    self.assertEqual(None, shortlink)

    mock_enqueue_event.assert_called_once_with('googs.com',
                                               'link.deleted',
                                               'link',
                                               {'shortpath': 'there',
                                                'created': str(test_shortlink.created),
                                                'modified': str(test_shortlink.modified),
                                                'id': '7',
                                                'visits_count': 0,
                                                'owner': 'kay@googs.com',
                                                'namespace': 'go',
                                                'destination_url': 'http://drive.com',
                                                'type': None})


@patch('shared_helpers.config.get_config', return_value={'sessions_secret': 'the_secret',
                                                         'admins': ['sam@googs.com']})
class TestLinkTransferHandlers(TrottoTestCase):
  blueprints_under_test = [handlers.routes]

  def setUp(self):
    super().setUp()

    self.test_user = User(id=777,
                          email='kay@googs.com',
                          organization='googs.com',
                          domain_type='corporate')
    self.test_user.put()

    # admin user
    User(email='sam@googs.com',
         organization='googs.com',
         domain_type='corporate'
         ).put()

    self.test_shortlink = ShortLink(id=7,
                                    organization='googs.com',
                                    owner=self.test_user.email,
                                    shortpath='there',
                                    shortpath_prefix='there',
                                    destination_url='http://drive.com')
    self.test_shortlink.put()

    self.in_an_hour = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    self.token_payload = {'exp': self.in_an_hour,
                          'sub': 'link:7',
                          'tp': 'transfer',
                          'o': 777,
                          'by': 777}

  def _get_transfer_token(self, jwt_token: Optional[str] = None) -> str:
    jwt_token = jwt_token or jwt.encode(self.token_payload, 'the_secret', algorithm='HS256')
    encoded = jwt_token.encode('utf-8')
    return base64.urlsafe_b64encode(encoded).decode('utf-8').strip('=')

  def test_get_transfer_link__authorized(self, _):
    next_year = datetime.datetime.utcnow().year + 1
    with freeze_time(datetime.datetime(next_year, 10, 1, 1, 0, 0)):
      response = self.testapp.post('/_/api/links/7/transfer_link',
                                   headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual(201, response.status_int)

    expected_jwt = jwt.encode({'exp': datetime.datetime(next_year, 10, 2, 1, 0, 0),
                               'sub': 'link:7',
                               'tp': 'transfer',
                               'o': self.test_user.id,
                               'by': self.test_user.id},
                              'the_secret',
                              algorithm='HS256')

    expected_url = f"http://localhost/_transfer/{self._get_transfer_token(expected_jwt)}"

    self.assertEqual({'url': expected_url},
                     response.json)

  def test_get_transfer_link__authorized_admin(self, _):
    next_year = datetime.datetime.utcnow().year + 1
    with freeze_time(datetime.datetime(next_year, 10, 1, 1, 0, 0)):
      response = self.testapp.post('/_/api/links/7/transfer_link',
                                   headers={'TROTTO_USER_UNDER_TEST': 'sam@googs.com'})

    self.assertEqual(201, response.status_int)

    expected_jwt = jwt.encode({'exp': datetime.datetime(next_year, 10, 2, 1, 0, 0),
                               'sub': 'link:7',
                               'tp': 'transfer',
                               'o': self.test_user.id,
                               'by': User.get_by_email_and_org('sam@googs.com', 'googs.com').id},
                              'the_secret',
                              algorithm='HS256')

    expected_url = f"http://localhost/_transfer/{self._get_transfer_token(expected_jwt)}"

    self.assertEqual({'url': expected_url},
                     response.json)

  def test_get_transfer_link__user_only_has_read_access(self, _):
    response = self.testapp.post('/_/api/links/7/transfer_link',
                                 headers={'TROTTO_USER_UNDER_TEST': 'jay@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

  def test_get_transfer_link__no_such_link(self, _):
    response = self.testapp.post('/_/api/links/10/transfer_link',
                                 headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

  def test_use_transfer_link__jwt_expired(self, _):
    minute_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
    self.token_payload.update({'exp': minute_ago})

    transfer_token = self._get_transfer_token()

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)
    self.assertEqual({'error_type': 'error_bar',
                      'error': 'Your transfer link has expired'},
                     response.json)

  def test_use_transfer_link__jwt_invalid_signature(self, _):
    invalid_jwt = jwt.encode(self.token_payload, 'no_secret', algorithm='HS256')
    transfer_token = self._get_transfer_token(invalid_jwt)

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

  def test_use_transfer_link__inapplicable_subject(self, _):
    self.token_payload.update({'sub': 'link_something:7'})

    transfer_token = self._get_transfer_token()

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

  def test_use_transfer_link__jwt_missing_claims(self, _):
    del self.token_payload['tp']

    transfer_token = self._get_transfer_token()

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

  def test_use_transfer_link__invalid_permission(self, _):
    self.token_payload.update({'tp': 'read'})

    transfer_token = self._get_transfer_token()

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

  def test_use_transfer_link__no_such_link(self, _):
    self.token_payload.update({'sub': 'link:20'})

    transfer_token = self._get_transfer_token()

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

  def test_use_transfer_link__owner_does_not_match(self, _):
    User(id=20,
         email='al@googs.com',
         organization='googs.com',
         domain_type='corporate'
         ).put()

    self.token_payload.update({'o': 20})

    transfer_token = self._get_transfer_token()

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)
    self.assertEqual({'error_type': 'error_bar',
                      'error': 'The owner of go/there has changed since your transfer link was created'},
                     response.json)

  def test_use_transfer_link__token_from_user_without_access(self, _):
    User(id=20,
         email='al@googs.com',
         organization='googs.com',
         domain_type='corporate'
         ).put()

    self.token_payload.update({'by': 20})

    transfer_token = self._get_transfer_token()

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)
    self.assertEqual({'error_type': 'error_bar',
                      'error': 'The user who created your transfer link no longer has edit rights for go/there'},
                     response.json)

  def test_use_transfer_link__accepting_user_in_wrong_org(self, _):
    transfer_token = self._get_transfer_token()

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@other.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

    link = ShortLink.get_by_id(7)

    self.assertEqual('kay@googs.com', link.owner)

  def test_use_transfer_link__success(self, _):
    transfer_token = self._get_transfer_token()

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'})
    self.assertEqual(201, response.status_int)

    updated_link = ShortLink.get_by_id(7)

    self.assertEqual('joe@googs.com', updated_link.owner)

  def test_use_transfer_link__success__generated_by_admin(self, _):
    self.token_payload.update({'by': User.get_by_email_and_org('sam@googs.com', 'googs.com').id})

    transfer_token = self._get_transfer_token()

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'})
    self.assertEqual(201, response.status_int)

    updated_link = ShortLink.get_by_id(7)

    self.assertEqual('joe@googs.com', updated_link.owner)

  def test_redirect_transfer_url__signed_in(self, _):
    response = self.testapp.get('/_transfer/my_token',
                                headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'})

    self.assertEqual(302, response.status_int)
    self.assertEqual('http://localhost/?transfer=my_token', response.location)

  def test_redirect_transfer_url__not_signed_in(self, _):
    response = self.testapp.get('/_transfer/my_token')

    self.assertEqual(302, response.status_int)
    self.assertEqual('http://localhost/_/auth/login?redirect_to=%2F_transfer%2Fmy_token%3F',
                     response.location)


class TestKeywordPunctuationSensitivityConfig(TrottoTestCase):

  blueprints_under_test = [handlers.routes]

  TEST_KEYWORD = 'meeting-notes'
  TEST_DESTINATION = 'https://docs.google.com/document/d/2Bd5X-6WFpRbafPgXax98GZenmCTZkTrNxotNvb8k2vI/edit'

  def _create_link(self, keyword):
    response = self.testapp.post_json('/_/api/links',
                                      {'shortpath': keyword,
                                       'destination': self.TEST_DESTINATION},
                                      headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    return response.json

  @patch('shared_helpers.config.get_organization_config',
         return_value={})
  def test_keyword_punctuation_sensitivity__not_specified(self, _):
    response = self._create_link(self.TEST_KEYWORD)

    self.assertEqual(self.TEST_KEYWORD, response.get('shortpath'))

    keyword_without_dashes = self.TEST_KEYWORD.replace('-', '')

    response = self._create_link(keyword_without_dashes)

    self.assertEqual(keyword_without_dashes, response.get('shortpath'))

  @patch('shared_helpers.config.get_organization_config',
         return_value={'keywords': {'punctuation_sensitive': False}})
  def test_keyword_punctuation_sensitivity__insensitive(self, _):
    response = self._create_link(self.TEST_KEYWORD)

    self.assertEqual(self.TEST_KEYWORD, response.get('shortpath'))

    keyword_without_dashes = self.TEST_KEYWORD.replace('-', '')

    response = self._create_link(keyword_without_dashes)

    self.assertIn(self.TEST_KEYWORD, response.get('error'))

    response = self.testapp.get('/_/api/links',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual(1, len(response.json))

    self.assertEqual(self.TEST_KEYWORD, response.json[0]['shortpath'])



BASE_URL = '/_/api/links'


@patch(
  'shared_helpers.config.get_config',
  return_value={'encryption_key': 'secret', 'admins': ['sam@googs.com']},
)
class TestHandlersPublicAPI(TrottoTestCase):
  """Testing only additional behaviour for public API"""
  blueprints_under_test = [handlers.routes]

  def setUp(self):
    super().setUp()

    self.token = ApiToken(
      key=generate_secret(64),
      organization='test_org',
    )

    self.token.put()

  def test_unathorized(self, _):
    """Tests all API endpoint with non-admin user"""
    for url, method in (
      (BASE_URL, 'POST'),
      (f'{BASE_URL}/1', 'PUT'),
      (f'{BASE_URL}/1', 'DELETE'),
      (BASE_URL, 'GET'),
    ):
      with self.subTest():
        response = self.testapp.request(
          url,
          method=method,
          expect_errors=True,
        )
        self.assertEqual(401, response.status_int)

  def test_invalid_token(self, _):
    """Tests all API endpoint with non-admin user"""
    for url, method in (
      (BASE_URL, 'POST'),
      (f'{BASE_URL}/1', 'PUT'),
      (f'{BASE_URL}/1', 'DELETE'),
      (BASE_URL, 'GET'),
    ):
      with self.subTest():
        response = self.testapp.request(
          url,
          method=method,
          headers={'Authorization': 'invalid'},
          expect_errors=True,
        )
        self.assertEqual(401, response.status_int)

  def test_create_link(self, _):
    response = self.testapp.post_json(
      BASE_URL,
      {
        'shortpath': 'there',
        'destination': 'http://example.com/there',
        'owner': 'john.doe@te.st',
      },
      headers={'Authorization': self.token.key},
    )

    self.assertEqual(201, response.status_int)

  def test_create_without_owner(self, _):
    response = self.testapp.post_json(
      BASE_URL,
      {
        'shortpath': 'there',
        'destination': 'http://example.com/there',
      },
      headers={'Authorization': self.token.key},
      expect_errors=True,
    )

    self.assertEqual(400, response.status_int)

  def test_get_list(self, _):
    """Testing successfull get for token_list"""
    link_list = [ShortLink(
      organization='test_org',
      owner='kay@googs.com',
      namespace='go',
      shortpath=f'there{index}',
      shortpath_prefix='there',
      destination_url='http://drive.com'
    ) for index in range(10)]
    for link in link_list:
      link.put()

    response = self.testapp.get(
      BASE_URL,
      headers={'Authorization': self.token.key},
    )

    self.assertEqual(200, response.status_int)
    response = json.loads(response.text)
    self.assertEqual(
      {link.id for link in link_list},
      {int(res_link['id']) for res_link in response}
    )

  def test_update_destination(self, _):
    existed_link = ShortLink(
      organization='test_org',
      owner='kay@googs.com',
      namespace='go',
      shortpath='existing',
      shortpath_prefix='there',
      destination_url='http://drive.com'
    )
    existed_link.put()
    response = self.testapp.put_json(
      f'{BASE_URL}/{existed_link.id}',
      {
        'destination': 'http://to.survive',
      },
      headers={'Authorization': self.token.key},
    )

    self.assertEqual(200, response.status_int)
    response = json.loads(response.text)
    self.assertEqual(existed_link.shortpath, response['shortpath'])
    self.assertEqual('http://to.survive', response['destination_url'])

  def test_delete(self, _):
    existed_link = ShortLink(
      organization='test_org',
      owner='kay@googs.com',
      namespace='go',
      shortpath='existing',
      shortpath_prefix='there',
      destination_url='http://drive.com'
    )
    existed_link.put()
    response = self.testapp.delete(
      f'{BASE_URL}/{existed_link.id}',
      headers={'Authorization': self.token.key},
    )

    self.assertEqual(200, response.status_int)

    response = self.testapp.get(
      BASE_URL,
      headers={'Authorization': self.token.key},
    )
    response = json.loads(response.text)

    self.assertNotIn(existed_link.id, {int(res_link['id']) for res_link in response})
