import datetime
import json
from mock import patch, call

from modules.data import get_models
from modules.users import handlers
from testing import TrottoTestCase


User = get_models('users').User


class TestUserHandlers(TrottoTestCase):

  blueprints_under_test = [handlers.routes]

  def setUp(self):
    super().setUp()

    self.ray = User(id=8675,
                    created=datetime.datetime(2021, 1, 11, 1, 2, 3),
                    email='ray@googs.com',
                    domain_type='corporate',
                    organization='googs.com')
    self.ray.put()

    self.kay = User(id=777,
                    created=datetime.datetime(2021, 1, 10, 1, 2, 3),
                    email='kay@googs.com',
                    domain_type='corporate',
                    organization='googs.com',
                    notifications={'some_announcement': 'dismissed'})
    self.kay.put()

    User(id=9000,
         created=datetime.datetime(2021, 1, 12, 1, 2, 3),
         email='jay@alph.com',
         domain_type='corporate',
         organization='alph.com').put()

  def test_user_info_endpoint(self):
    response = self.testapp.get('/_/api/users/me',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual(json.loads(response.text),
                     {'id': 777,
                      'created': '2021-01-10T01:02:03',
                      'email': 'kay@googs.com',
                      'organization': 'googs.com',
                      'role': None,
                      'admin': False,
                      'notifications': {'some_announcement': 'dismissed'},
                      'org_edit_mode': 'owners_and_admins_only',
                      'read_only_mode': None,
                      'info_bar': None,
                      'keywords_validation_regex': '[^0-9a-zA-Z\\-\\/%]'})

    response = self.testapp.get('/_/api/users/me',
                                headers={'TROTTO_USER_UNDER_TEST': 'ray@googs.com'})

    self.assertEqual(json.loads(response.text),
                     {'id': 8675,
                      'created': '2021-01-11T01:02:03',
                      'email': 'ray@googs.com',
                      'organization': 'googs.com',
                      'role': None,
                      'admin': False,
                      'notifications': {},
                      'org_edit_mode': 'owners_and_admins_only',
                      'read_only_mode': None,
                      'info_bar': None,
                      'keywords_validation_regex': '[^0-9a-zA-Z\\-\\/%]'})

  @patch('modules.users.handlers.is_user_admin', return_value=True)
  def test_user_info_endpoint__by_user_id__is_admin(self, mock_is_user_admin):
    response = self.testapp.get('/_/api/users/777',
                                headers={'TROTTO_USER_UNDER_TEST': 'ray@googs.com'})

    self.assertEqual(json.loads(response.text),
                     {'id': 777,
                      'created': '2021-01-10T01:02:03',
                      'email': 'kay@googs.com',
                      'organization': 'googs.com',
                      'role': None,
                      'admin': True,
                      'notifications': {'some_announcement': 'dismissed'}})


    self.assertEqual([call(self.ray, 'googs.com'),
                      call(self.kay)],
                     mock_is_user_admin.call_args_list)

  @patch('modules.users.handlers.is_user_admin', return_value=False)
  def test_user_info_endpoint__by_user_id__is_not_admin(self, mock_is_user_admin):
    response = self.testapp.get('/_/api/users/777',
                                headers={'TROTTO_USER_UNDER_TEST': 'ray@googs.com'},
                                expect_errors=True)

    self.assertEqual(403, response.status_int)

    mock_is_user_admin.assert_called_once_with(self.ray, 'googs.com')

  @patch('modules.users.handlers.is_user_admin', return_value=False)
  def test_user_info_endpoint__by_user_id__different_org(self, mock_is_user_admin):
    response = self.testapp.get('/_/api/users/9000',
                                headers={'TROTTO_USER_UNDER_TEST': 'ray@googs.com'},
                                expect_errors=True)

    self.assertEqual(403, response.status_int)

    mock_is_user_admin.assert_called_once_with(self.ray, 'alph.com')

  @patch('modules.users.handlers.is_user_admin', return_value=True)
  def test_user_info_endpoint__by_user_id__no_such_user(self, mock_is_user_admin):
    response = self.testapp.get('/_/api/users/8',
                                headers={'TROTTO_USER_UNDER_TEST': 'ray@googs.com'},
                                expect_errors=True)

    self.assertEqual(403, response.status_int)

    mock_is_user_admin.assert_not_called()

  @patch('modules.users.handlers.is_user_admin', return_value=True)
  def test_users_endpoint__is_admin(self, mock_is_user_admin):
    response = self.testapp.get('/_/api/organizations/mine/users',
                                headers={'TROTTO_USER_UNDER_TEST': 'ray@googs.com'})

    self.assertCountEqual(json.loads(response.text),
                          [{'id': 8675,
                            'created': '2021-01-11T01:02:03',
                            'email': 'ray@googs.com',
                            'organization': 'googs.com',
                            'role': None,
                            'admin': True,
                            'notifications': {}},
                           {'id': 777,
                            'created': '2021-01-10T01:02:03',
                            'email': 'kay@googs.com',
                            'organization': 'googs.com',
                            'role': None,
                            'admin': True,
                            'notifications': {'some_announcement': 'dismissed'}}])

    self.assertCountEqual([call(self.ray),
                           call(self.ray),
                           call(self.kay)],
                          mock_is_user_admin.call_args_list)

  @patch('modules.users.handlers.is_user_admin', return_value=False)
  def test_users_endpoint__is_not_admin(self, mock_is_user_admin):
    response = self.testapp.get('/_/api/organizations/mine/users',
                                headers={'TROTTO_USER_UNDER_TEST': 'ray@googs.com'},
                                expect_errors=True)

    self.assertEqual(403, response.status_int)

    mock_is_user_admin.assert_called_once_with(self.ray)

  @patch('modules.users.handlers.is_user_admin', return_value=True)
  @patch('modules.users.handlers.get_admin_ids', return_value=[1, 8675])
  def test_users_endpoint__with_admin_service__is_admin(self, mock_get_admin_ids, mock_is_user_admin):
    response = self.testapp.get('/_/api/organizations/mine/users',
                                headers={'TROTTO_USER_UNDER_TEST': 'ray@googs.com'})

    self.assertCountEqual(json.loads(response.text),
                          [{'id': 8675,
                            'created': '2021-01-11T01:02:03',
                            'email': 'ray@googs.com',
                            'organization': 'googs.com',
                            'role': None,
                            'admin': True,
                            'notifications': {}},
                           {'id': 777,
                            'created': '2021-01-10T01:02:03',
                            'email': 'kay@googs.com',
                            'organization': 'googs.com',
                            'role': None,
                            'admin': False,
                            'notifications': {'some_announcement': 'dismissed'}}])

    mock_get_admin_ids.assert_called_once_with('googs.com')
    mock_is_user_admin.assert_called_once_with(self.ray)
