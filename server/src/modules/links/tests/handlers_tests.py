import base64
import datetime
import json

from freezegun import freeze_time
import jwt
from mock import patch, call

from modules.data import get_models
from modules.links import handlers
from testing import TrottoTestCase

ShortLink = get_models('links').ShortLink
User = get_models('users').User


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

    mock_create_short_link.return_value = mock_shortlink

    response = self.testapp.post_json('/_/api/links',
                                      {'shortpath': 'there',
                                       'destination': 'http://example.com/there'},
                                      headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual({'id': 123,
                      'created': '2018-10-01 00:00:00',
                      'modified': '2018-11-01 00:00:00',
                      'owner': 'kay@googs.com',
                      'namespace': 'go',
                      'shortpath': 'there',
                      'destination_url': 'http://example.com/there',
                      'visits_count': 0},
                     json.loads(response.text))

    self.assertEqual(mock_create_short_link.call_args_list,
                     [call('googs.com', 'kay@googs.com', 'go', 'there', 'http://example.com/there')])

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

    self.assertCountEqual([{'id': 1,
                            'created': '2018-10-01 00:00:00',
                            'modified': str(modified_datetime),
                            'mine': True,
                            'owner': 'kay@googs.com',
                            'namespace': 'go',
                            'shortpath': 'there',
                            'destination_url': 'http://example.com',
                            'visits_count': 0},
                           {'id': 2,
                            'created': '2018-11-01 00:00:00',
                            'modified': str(modified_datetime),
                            'mine': False,
                            'owner': 'jay@googs.com',
                            'namespace': 'go',
                            'shortpath': 'here',
                            'destination_url': 'http://gmail.com',
                            'visits_count': 0},
                           {'id': 4,
                            'created': '2019-11-01 00:00:00',
                            'modified': str(modified_datetime),
                            'mine': False,
                            'owner': 'jay@googs.com',
                            'namespace': 'eng',
                            'shortpath': '1',
                            'destination_url': 'http://1.com',
                            'visits_count': 0}],
                          json.loads(response.text))

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

    mock_enqueue_event.assert_called_once_with('link.deleted',
                                               'link',
                                               {'shortpath': 'there',
                                                'created': str(test_shortlink.created),
                                                'modified': str(test_shortlink.modified),
                                                'id': 7,
                                                'visits_count': 0,
                                                'owner': 'kay@googs.com',
                                                'namespace': 'go',
                                                'destination_url': 'http://drive.com'})


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

    expected_url = f"http://localhost/_transfer/{base64.urlsafe_b64encode(expected_jwt).decode('utf-8').strip('=')}"

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
                               'by': User.get_by_email('sam@googs.com').id},
                              'the_secret',
                              algorithm='HS256')

    expected_url = f"http://localhost/_transfer/{base64.urlsafe_b64encode(expected_jwt).decode('utf-8').strip('=')}"

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

    transfer_token = base64.urlsafe_b64encode(jwt.encode(self.token_payload,
                                                         'the_secret',
                                                         algorithm='HS256')
                                              ).decode('utf-8').strip('=')

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)
    self.assertEqual({'error_type': 'error_bar',
                      'error': 'Your transfer link has expired'},
                     response.json)

  def test_use_transfer_link__jwt_invalid_signature(self, _):
    transfer_token = base64.urlsafe_b64encode(jwt.encode(self.token_payload,
                                                         'no_secret',
                                                         algorithm='HS256')
                                              ).decode('utf-8').strip('=')

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

  def test_use_transfer_link__inapplicable_subject(self, _):
    self.token_payload.update({'sub': 'link_something:7'})

    transfer_token = base64.urlsafe_b64encode(jwt.encode(self.token_payload,
                                                         'the_secret',
                                                         algorithm='HS256')
                                              ).decode('utf-8').strip('=')

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

  def test_use_transfer_link__jwt_missing_claims(self, _):
    del self.token_payload['tp']

    transfer_token = base64.urlsafe_b64encode(jwt.encode(self.token_payload,
                                                         'the_secret',
                                                         algorithm='HS256')
                                              ).decode('utf-8').strip('=')

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

  def test_use_transfer_link__invalid_permission(self, _):
    self.token_payload.update({'tp': 'read'})

    transfer_token = base64.urlsafe_b64encode(jwt.encode(self.token_payload,
                                                         'the_secret',
                                                         algorithm='HS256')
                                              ).decode('utf-8').strip('=')

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

  def test_use_transfer_link__no_such_link(self, _):
    self.token_payload.update({'sub': 'link:20'})

    transfer_token = base64.urlsafe_b64encode(jwt.encode(self.token_payload,
                                                         'the_secret',
                                                         algorithm='HS256')
                                              ).decode('utf-8').strip('=')

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

    transfer_token = base64.urlsafe_b64encode(jwt.encode(self.token_payload,
                                                         'the_secret',
                                                         algorithm='HS256')
                                              ).decode('utf-8').strip('=')

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

    transfer_token = base64.urlsafe_b64encode(jwt.encode(self.token_payload,
                                                         'the_secret',
                                                         algorithm='HS256')
                                              ).decode('utf-8').strip('=')

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)
    self.assertEqual({'error_type': 'error_bar',
                      'error': 'The user who created your transfer link no longer has edit rights for go/there'},
                     response.json)

  def test_use_transfer_link__accepting_user_in_wrong_org(self, _):
    transfer_token = base64.urlsafe_b64encode(jwt.encode(self.token_payload,
                                                         'the_secret',
                                                         algorithm='HS256')
                                              ).decode('utf-8').strip('=')

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@other.com'},
                                 expect_errors=True)
    self.assertEqual(403, response.status_int)

    link = ShortLink.get_by_id(7)

    self.assertEqual('kay@googs.com', link.owner)

  def test_use_transfer_link__success(self, _):
    transfer_token = base64.urlsafe_b64encode(jwt.encode(self.token_payload,
                                                         'the_secret',
                                                         algorithm='HS256')
                                              ).decode('utf-8').strip('=')

    response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'})
    self.assertEqual(201, response.status_int)

    updated_link = ShortLink.get_by_id(7)

    self.assertEqual('joe@googs.com', updated_link.owner)

  def test_use_transfer_link__success__generated_by_admin(self, _):
    self.token_payload.update({'by': User.get_by_email('sam@googs.com').id})

    transfer_token = base64.urlsafe_b64encode(jwt.encode(self.token_payload,
                                                         'the_secret',
                                                         algorithm='HS256')
                                              ).decode('utf-8').strip('=')

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
