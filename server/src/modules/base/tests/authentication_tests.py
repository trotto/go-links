from mock import Mock, patch

from modules.base import authentication
from shared_helpers.config import ServiceNotConfiguredError

from testing import TrottoTestCase


class TestFunctions(TrottoTestCase):

  @patch('modules.base.authentication.service_get', return_value={'authentication_methods': ['google']})
  def test_get_allowed_authentication_methods__admin_service_configured(self, mock_service_get):
    self.assertEqual(['google'],
                     authentication.get_allowed_authentication_methods('example.com'))

    mock_service_get.assert_called_once_with('admin', '/organizations/example.com/settings')

  @patch('modules.base.authentication.service_get', return_value={})
  def test_get_allowed_authentication_methods__admin_service_configured__no_methods(self, mock_service_get):
    self.assertEqual(None,
                     authentication.get_allowed_authentication_methods('example.com'))

    mock_service_get.assert_called_once_with('admin', '/organizations/example.com/settings')

  @patch('modules.base.authentication.service_get', side_effect=ServiceNotConfiguredError)
  def test_get_allowed_authentication_methods__admin_service_not_configured(self, mock_service_get):
    self.assertEqual(None,
                     authentication.get_allowed_authentication_methods('example.com'))

    mock_service_get.assert_called_once_with('admin', '/organizations/example.com/settings')

  @staticmethod
  def _get_mock_request(host, headers=None):
    mock_request = Mock()

    mock_request.host = host
    mock_request.headers = headers or {}

    return mock_request

  def test_get_host_for_request__no_override(self):
    mock_request = self._get_mock_request('trot.to')

    self.assertEqual('https://trot.to',
                     authentication.get_host_for_request(mock_request))

  def test_get_host_for_request__no_override__localhost(self):
    mock_request = self._get_mock_request('localhost:9095')

    self.assertEqual('http://localhost:9095',
                     authentication.get_host_for_request(mock_request))

  def test_get_host_for_request__override(self):
    mock_request = self._get_mock_request('localhost:9095', {'X-Upstream-Host': 'upstream.trot.to'})

    self.assertEqual('https://upstream.trot.to',
                     authentication.get_host_for_request(mock_request))

  def test_get_host_for_request__override__no_host_attribute(self):
    mock_request = self._get_mock_request(None, {'X-Upstream-Host': 'upstream.trot.to'})

    self.assertEqual('https://upstream.trot.to',
                     authentication.get_host_for_request(mock_request))
