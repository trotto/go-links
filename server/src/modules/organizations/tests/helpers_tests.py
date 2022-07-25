from mock import patch

from modules.organizations import helpers
from shared_helpers.config import ServiceNotConfiguredError

from testing import TrottoTestCase


class TestHelperFunctions(TrottoTestCase):

  @patch('modules.organizations.helpers.service_get', return_value={'authentication_methods': ['google']})
  def test_get_org_settings__admin_service_configured(self, mock_service_get):
    self.assertEqual({'authentication_methods': ['google']},
                     helpers.get_org_settings('googs.com'))

    mock_service_get.assert_called_once_with('admin', '/organizations/googs.com/settings')

  @patch('modules.organizations.helpers.service_get', side_effect=ServiceNotConfiguredError)
  def test_get_org_settings__admin_service_not_configured(self, mock_service_get):
    self.assertEqual({},
                     helpers.get_org_settings('googs.com'))

    mock_service_get.assert_called_once_with('admin', '/organizations/googs.com/settings')
