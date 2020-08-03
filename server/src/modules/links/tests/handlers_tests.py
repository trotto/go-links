import datetime
import json

from freezegun import freeze_time
from mock import patch, call

from modules.data import get_models
from modules.links import handlers
from testing import TrottoTestCase


ShortLink = get_models('links').ShortLink


class TestHandlers(TrottoTestCase):

  blueprints_under_test = [handlers.routes]

  @patch('modules.links.helpers.create_short_link')
  def test_create_link(self, mock_create_short_link):
    mock_shortlink = ShortLink(id=123,
                               created=datetime.datetime(2018, 10, 1),
                               modified=datetime.datetime(2018, 11, 1),
                               organization='googs.com',
                               owner='kay@googs.com',
                               shortpath='there',
                               destination_url='http://example.com/there')

    mock_create_short_link.return_value = mock_shortlink

    response = self.testapp.post_json('/_/api/links',
                                      {'shortpath': 'there',
                                       'destination': 'http://example.com/there'},
                                      headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual({'oid': 123,
                      'created': '2018-10-01 00:00:00',
                      'modified': '2018-11-01 00:00:00',
                      'owner': 'kay@googs.com',
                      'shortpath': 'there',
                      'destination_url': 'http://example.com/there',
                      'visits_count': 0},
                     json.loads(response.text))

    self.assertEqual(mock_create_short_link.call_args_list,
                     [call('googs.com', 'kay@googs.com', 'there', 'http://example.com/there')])

  def test_create_link__no_patching(self):
    self.testapp.post_json('/_/api/links',
                           {'shortpath': 'favorites',
                            'destination': 'http://example.com'},
                           headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    shortlinks = ShortLink._get_all()

    self.assertEqual(1, len(shortlinks))

    shortlink = shortlinks[0]

    self.assertEqual('favorites', shortlink.shortpath)
    self.assertEqual('http://example.com', shortlink.destination_url)

  def test_get_shortlinks_for_user(self):
    modified_datetime = datetime.datetime.utcnow() + datetime.timedelta(days=2)

    with freeze_time(modified_datetime):
      ShortLink(id=1,
                created=datetime.datetime(2018, 10, 1),
                organization='googs.com',
                owner='kay@googs.com',
                shortpath='there',
                destination_url='http://example.com'
                ).put()
      ShortLink(id=2,
                created=datetime.datetime(2018, 11, 1),
                organization='googs.com',
                owner='jay@googs.com',
                shortpath='here',
                destination_url='http://gmail.com'
                ).put()
      ShortLink(id=3,
                organization='widgets.com',
                owner='el@widgets.com',
                shortpath='elsewhere',
                destination_url='http://drive.com'
                ).put()

    response = self.testapp.get('/_/api/links',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual([{'oid': 1,
                       'created': '2018-10-01 00:00:00',
                       'modified': str(modified_datetime),
                       'mine': True,
                       'owner': 'kay@googs.com',
                       'shortpath': 'there',
                       'destination_url': 'http://example.com',
                       'visits_count': 0},
                      {'oid': 2,
                       'created': '2018-11-01 00:00:00',
                       'modified': str(modified_datetime),
                       'mine': False,
                       'owner': 'jay@googs.com',
                       'shortpath': 'here',
                       'destination_url': 'http://gmail.com',
                       'visits_count': 0}],
                     json.loads(response.text))

  def test_update_link__go_link__successful(self):
    ShortLink(id=7,
              organization='googs.com',
              owner='kay@googs.com',
              shortpath='there',
              destination_url='http://example.com'
              ).put()

    self.testapp.put_json('/_/api/links/7',
                          {'destination': 'http://boop.com'},
                          headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    shortlink = ShortLink.get_by_id(7)

    self.assertEqual('http://boop.com', shortlink.destination_url)

  def test_created_and_modified_date_tracking(self):
    time_1 = datetime.datetime.utcnow() + datetime.timedelta(days=2)
    time_2 = datetime.datetime.utcnow() + datetime.timedelta(days=4)

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
      self.testapp.put_json('/_/api/links/%s' % (link['oid']),
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
              shortpath='there',
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
              shortpath='there',
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
              shortpath='there',
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
              shortpath='there',
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
              shortpath='there',
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
              shortpath='there',
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
                               shortpath='there',
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
                                                'oid': 7,
                                                'visits_count': 0,
                                                'owner': 'kay@googs.com',
                                                'destination_url': 'http://drive.com'})
