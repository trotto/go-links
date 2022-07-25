from mock import patch

from modules.data import get_models
from modules.users import helpers
from shared_helpers.config import ServiceNotConfiguredError

models = get_models('users')

from testing import TrottoTestCase


class TestHelperFunctions(TrottoTestCase):

  database = 'postgres'

  def test_get_users_by_organization(self):
    users = [models.User(id=1,
                         email='kay@googs.com',
                         organization='googs.com',
                         domain_type='corporate'),
             models.User(id=2,
                         email='kay@alph.com',
                         organization='alph.com',
                         domain_type='corporate'),
             models.User(id=3,
                         email='jay@googs.com',
                         organization='googs.com',
                         domain_type='corporate')]

    for u in users:
      u.put()

    org_users = helpers.get_users_by_organization('googs.com')

    self.assertEqual([users[0], users[2]],
                     sorted([u for u in org_users], key=lambda u: u.id))

  @patch('modules.users.helpers.service_get', return_value=[{'id': 1}, {'id': 4}, {'id': 2}])
  def test_get_admin_ids__admin_service_configured(self, mock_service_get):
    self.assertEqual([1, 4, 2],
                     helpers.get_admin_ids('googs.com'))

    mock_service_get.assert_called_once_with('admin', '/organizations/googs.com/users?role=admin')

  @patch('modules.users.helpers.service_get', return_value=[{'id': 1}, {'id': 4}, {'id': 2}])
  def test_get_admin_ids__admin_service_configured__url_encoded_char(self, mock_service_get):
    self.assertEqual([1, 4, 2],
                     helpers.get_admin_ids('j@gmail.com'))

    mock_service_get.assert_called_once_with('admin', '/organizations/j%40gmail.com/users?role=admin')

  @patch('modules.users.helpers.service_get', side_effect=ServiceNotConfiguredError)
  def test_get_admin_ids__admin_service_not_configured(self, mock_service_get):
    self.assertEqual(None,
                     helpers.get_admin_ids('googs.com'))

    mock_service_get.assert_called_once_with('admin', '/organizations/googs.com/users?role=admin')

  @patch('shared_helpers.config.get_organization_config', return_value={'admins': ['may@googs.com',
                                                                                   'sam@googs.com']})
  @patch('modules.users.helpers.service_get', side_effect=ServiceNotConfiguredError)
  def test_is_user_admin__is_admin(self, mock_service_get, mock_get_organization_config):
    test_user = models.User(email='may@googs.com',
                            organization='googs.com')

    self.assertEqual(True,
                     helpers.is_user_admin(test_user))

    mock_service_get.assert_called_once_with('admin', '/organizations/googs.com/users?role=admin')
    mock_get_organization_config.assert_called_once_with('googs.com')

  @patch('shared_helpers.config.get_organization_config', return_value={'admins': ['may@googs.com',
                                                                                   'sam@googs.com']})
  @patch('modules.users.helpers.service_get', side_effect=ServiceNotConfiguredError)
  def test_is_user_admin__is_not_admin(self, mock_service_get, mock_get_organization_config):
    test_user = models.User(email='jay@googs.com',
                            organization='googs.com')

    self.assertEqual(False,
                     helpers.is_user_admin(test_user))

    mock_service_get.assert_called_once_with('admin', '/organizations/googs.com/users?role=admin')
    mock_get_organization_config.assert_called_once_with('googs.com')

  @patch('shared_helpers.config.get_organization_config', return_value={'admins': ['may@googs.com',
                                                                                   'sam@googs.com']})
  @patch('modules.users.helpers.service_get', side_effect=ServiceNotConfiguredError)
  def test_is_user_admin__is_admin_for_different_org(self, mock_service_get, mock_get_organization_config):
    test_user = models.User(email='may@googs.com',
                            organization='googs.com')

    self.assertEqual(False,
                     helpers.is_user_admin(test_user, 'alph.com'))

    mock_service_get.assert_not_called()
    mock_get_organization_config.assert_not_called()

  @patch('shared_helpers.config.get_organization_config', return_value={'admins': ['may@googs.com',
                                                                                   'sam@googs.com']})
  @patch('modules.users.helpers.service_get', return_value=[{'id': 1}, {'id': 3}, {'id': 2}])
  def test_is_user_admin__with_admin_service__is_admin(self, mock_service_get, mock_get_organization_config):
    test_user = models.User(id=3,
                            email='may@googs.com',
                            organization='googs.com')

    self.assertEqual(True,
                     helpers.is_user_admin(test_user))

    mock_service_get.assert_called_once_with('admin', '/organizations/googs.com/users?role=admin')
    mock_get_organization_config.assert_not_called()

  @patch('shared_helpers.config.get_organization_config', return_value={'admins': ['may@googs.com',
                                                                                   'sam@googs.com']})
  @patch('modules.users.helpers.service_get', return_value=[{'id': 1}, {'id': 4}, {'id': 2}])
  def test_is_user_admin__with_admin_service__is_not_admin(self, mock_service_get, mock_get_organization_config):
    test_user = models.User(id=3,
                            email='may@googs.com',
                            organization='googs.com')

    self.assertEqual(False,
                     helpers.is_user_admin(test_user))

    mock_service_get.assert_called_once_with('admin', '/organizations/googs.com/users?role=admin')
    mock_get_organization_config.assert_not_called()
