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

  @patch('modules.base.authentication.service_get', return_value={'authentication_methods': ['google']})
  def test_get_allowed_authentication_methods__admin_service_configured__url_encoded_char(self, mock_service_get):
    self.assertEqual(['google'],
                     authentication.get_allowed_authentication_methods('j@gmail.com'))

    mock_service_get.assert_called_once_with('admin', '/organizations/j%40gmail.com/settings')

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

  def test_get_user_email__success__gmail(self):
    mock_oauth_credentials = Mock()
    mock_oauth_credentials.id_token = {'email_verified': True,
                                       'hd': None,
                                       'email': 'sam@gmail.com'}

    self.assertEqual('sam@gmail.com',
                     authentication.get_user_email(mock_oauth_credentials))

  def test_get_user_email__success__google_workspace(self):
    mock_oauth_credentials = Mock()
    mock_oauth_credentials.id_token = {'email_verified': True,
                                       'hd': 'googs.com',
                                       'email': 'bill@googs.com'}

    self.assertEqual('bill@googs.com',
                     authentication.get_user_email(mock_oauth_credentials))

  def test_get_user_email__success__mixed_case(self):
    mock_oauth_credentials = Mock()
    mock_oauth_credentials.id_token = {'email_verified': True,
                                       'hd': None,
                                       'email': 'Sam@Gmail.com'}

    self.assertEqual('sam@gmail.com',
                     authentication.get_user_email(mock_oauth_credentials))

  def test_get_user_email__email_not_verified(self):
    mock_oauth_credentials = Mock()
    mock_oauth_credentials.id_token = {'email_verified': False,
                                       'hd': 'googs.com',
                                       'email': 'bill@googs.com'}

    self.assertEqual(None,
                     authentication.get_user_email(mock_oauth_credentials))

  def test_get_user_email__not_gmail_or_google_workspace(self):
    mock_oauth_credentials = Mock()
    mock_oauth_credentials.id_token = {'email_verified': True,
                                       'hd': None,
                                       'email': 'case3@googs.com'}

    self.assertEqual(None,
                     authentication.get_user_email(mock_oauth_credentials))

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
