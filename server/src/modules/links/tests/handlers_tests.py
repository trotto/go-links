import datetime
import json
import os
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from mock import patch, call
import webtest

from modules.links import handlers
from modules.links import models

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

  @patch('modules.links.helpers.create_short_link')
  def test_create_link(self, mock_create_short_link):
    mock_shortlink = models.ShortLink(id=123,
                                      created=datetime.datetime(2018, 10, 1),
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

    shortlinks = models.ShortLink.query().fetch(limit=None)

    self.assertEqual(1, len(shortlinks))

    shortlink = shortlinks[0]

    self.assertEqual('favorites', shortlink.shortpath)
    self.assertEqual('http://example.com', shortlink.destination_url)

  def test_get_shortlinks_for_user(self):
    ndb.put_multi([models.ShortLink(id=1,
                                    created=datetime.datetime(2018, 10, 1),
                                    organization='googs.com',
                                    owner='kay@googs.com',
                                    shortpath='there',
                                    destination_url='http://example.com'),
                   models.ShortLink(id=2,
                                    created=datetime.datetime(2018, 11, 1),
                                    organization='googs.com',
                                    owner='jay@googs.com',
                                    shortpath='here',
                                    destination_url='http://gmail.com'),
                   models.ShortLink(id=3,
                                    organization='widgets.com',
                                    owner='el@widgets.com',
                                    shortpath='elsewhere',
                                    destination_url='http://drive.com')])

    response = self.testapp.get('/_/api/links',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual([{'oid': 1,
                       'created': '2018-10-01 00:00:00',
                       'mine': True,
                       'owner': 'kay@googs.com',
                       'shortpath': 'there',
                       'destination_url': 'http://example.com',
                       'visits_count': 0},
                      {'oid': 2,
                       'created': '2018-11-01 00:00:00',
                       'mine': False,
                       'owner': 'jay@googs.com',
                       'shortpath': 'here',
                       'destination_url': 'http://gmail.com',
                       'visits_count': 0}],
                     json.loads(response.text))

  def test_update_link__go_link__successful(self):
    models.ShortLink(id=7,
                     organization='googs.com',
                     owner='kay@googs.com',
                     shortpath='there',
                     destination_url='http://example.com'
                     ).put()

    self.testapp.put_json('/_/api/links/7',
                          {'destination': 'http://boop.com'},
                          headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    shortlink = models.ShortLink.get_by_id(7)

    self.assertEqual('http://boop.com', shortlink.destination_url)

  def test_update_link__go_link_of_other_user__is_not_admin(self):
    models.ShortLink(id=7,
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

    shortlink = models.ShortLink.get_by_id(7)

    self.assertEqual('http://drive.com', shortlink.destination_url)

  @patch('modules.users.helpers.is_user_admin', return_value=True)
  def test_update_link__go_link_of_other_user__is_admin(self, mock_is_user_admin):
    models.ShortLink(id=7,
                     organization='googs.com',
                     owner='kay@googs.com',
                     shortpath='there',
                     destination_url='http://drive.com'
                     ).put()

    self.testapp.put_json('/_/api/links/7',
                          {'destination': 'http://boop.com'},
                          headers={'TROTTO_USER_UNDER_TEST': 'rex@googs.com'})

    shortlink = models.ShortLink.get_by_id(7)

    self.assertEqual('http://boop.com', shortlink.destination_url)

    self.assertEqual(1, mock_is_user_admin.call_count)
    self.assertEqual('rex@googs.com', mock_is_user_admin.call_args[0][0].email)

  @patch('modules.users.helpers.is_user_admin', return_value=True)
  def test_update_link__go_link_of_other_user__is_admin_for_different_org(self, mock_is_user_admin):
    models.ShortLink(id=7,
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

    shortlink = models.ShortLink.get_by_id(7)

    self.assertEqual('http://drive.com', shortlink.destination_url)

  def test_update_link__go_link_of_other_company(self):
    models.ShortLink(id=7,
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

    shortlink = models.ShortLink.get_by_id(7)

    self.assertEqual('http://drive.com', shortlink.destination_url)
