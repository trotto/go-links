import datetime
import unittest

from flask import Blueprint, request, jsonify
from freezegun import freeze_time
from mock import Mock, patch
import jwt
from requests.exceptions import HTTPError

from shared_helpers import services
from testing import TrottoTestCase, LIVE_APP_HOST


class TestFunctions(unittest.TestCase):

  @patch('shared_helpers.services.get_service_config', return_value={'signing_secret': 'so_secret'})
  def test__create_internal_token(self, mock_get_service_config):
    now = datetime.datetime.now(datetime.timezone.utc)

    with freeze_time(now):
      token = services._create_internal_token('my_service', {'id': 1})

      self.assertEqual({'exp': int(now.timestamp()) + 30,
                        'id': 1},
                       jwt.decode(token, 'so_secret', algorithms=['HS256']))

    with freeze_time(now + datetime.timedelta(seconds=40)):
      with self.assertRaises(jwt.exceptions.ExpiredSignatureError):
        jwt.decode(token, 'so_secret', algorithms=['HS256'])

    mock_get_service_config.assert_called_once_with('my_service')

  @patch('shared_helpers.services.requests.get')
  @patch('shared_helpers.services._create_internal_token', return_value='internal_token')
  @patch('shared_helpers.services.get_service_config', return_value={'base_url': 'https://trot.to'})
  def test_get__basic(self, mock_get_service_config, mock_create_internal_token, mock_requests_get):
    mock_response = Mock()
    mock_response.json.return_value = {'id': 1}

    mock_requests_get.return_value = mock_response

    self.assertEqual({'id': 1},
                     services.get('my_service', 'api/users'))

    mock_get_service_config.assert_called_once_with('my_service')
    mock_create_internal_token.assert_called_once_with('my_service', {'url': 'https://trot.to/api/users'})
    mock_requests_get.assert_called_once_with('https://trot.to/api/users',
                                              headers={'X-Token': 'internal_token'})

  @patch('shared_helpers.services.requests.get')
  @patch('shared_helpers.services._create_internal_token', return_value='internal_token')
  @patch('shared_helpers.services.get_service_config', return_value={'base_url': 'https://trot.to/'})
  def test_get__trailing_and_leading_slashes(self,
                                             mock_get_service_config, mock_create_internal_token, mock_requests_get):
    mock_response = Mock()
    mock_response.json.return_value = {'id': 1}

    mock_requests_get.return_value = mock_response

    self.assertEqual({'id': 1},
                     services.get('my_service', '/api/users'))

    mock_get_service_config.assert_called_once_with('my_service')
    mock_create_internal_token.assert_called_once_with('my_service', {'url': 'https://trot.to/api/users'})
    mock_requests_get.assert_called_once_with('https://trot.to/api/users',
                                              headers={'X-Token': 'internal_token'})

  @patch('shared_helpers.services.requests.get')
  @patch('shared_helpers.services._create_internal_token', return_value='internal_token')
  @patch('shared_helpers.services.get_service_config', return_value={'base_url': 'https://trot.to'})
  def test_get__http_error(self, mock_get_service_config, mock_create_internal_token, mock_requests_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = HTTPError

    mock_requests_get.return_value = mock_response

    with self.assertRaises(HTTPError):
      services.get('my_service', 'api/users')

    mock_get_service_config.assert_called_once_with('my_service')
    mock_create_internal_token.assert_called_once_with('my_service', {'url': 'https://trot.to/api/users'})
    mock_requests_get.assert_called_once_with('https://trot.to/api/users',
                                              headers={'X-Token': 'internal_token'})

  def test_validate_internal_request__no_token(self):
    mock_request = Mock()

    mock_request.headers = {}

    with self.assertRaises(services.InvalidInternalToken) as cm:
      services.validate_internal_request(mock_request)

    self.assertEqual('no token',
                     str(cm.exception))

  @patch('shared_helpers.services.get_config_by_key_path', return_value='so_secret')
  def test_validate_internal_request__invalid_signature__wrong_secret(self, mock_get_config_by_key_path):
    token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
                        'url': 'https://trot.to/api/users'},
                       'a_secret',
                       algorithm='HS256')

    mock_request = Mock()

    mock_request.headers = {'X-Token': token}
    mock_request.url = 'https://trot.to/api/users'

    with self.assertRaises(services.InvalidInternalToken) as cm:
      services.validate_internal_request(mock_request)

    self.assertEqual('invalid signature',
                     str(cm.exception))

    mock_get_config_by_key_path.assert_called_once_with(['signing_secret'])

  @patch('shared_helpers.services.get_config_by_key_path', return_value='so_secret')
  def test_validate_internal_request__invalid_signature__no_exp(self, mock_get_config_by_key_path):
    token = jwt.encode({'url': 'https://trot.to/api/users'},
                       'so_secret',
                       algorithm='HS256')

    mock_request = Mock()

    mock_request.headers = {'X-Token': token}
    mock_request.url = 'https://trot.to/api/users'

    with self.assertRaises(services.InvalidInternalToken) as cm:
      services.validate_internal_request(mock_request)

    self.assertEqual('missing exp',
                     str(cm.exception))

    mock_get_config_by_key_path.assert_called_once_with(['signing_secret'])

  @patch('shared_helpers.services.get_config_by_key_path', return_value='so_secret')
  def test_validate_internal_request__expired_token(self, mock_get_config_by_key_path):
    token = jwt.encode({'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=1),
                        'url': 'https://trot.to/api/users'},
                       'so_secret',
                       algorithm='HS256')

    mock_request = Mock()

    mock_request.headers = {'X-Token': token}
    mock_request.url = 'https://trot.to/api/users'

    with self.assertRaises(services.InvalidInternalToken) as cm:
      services.validate_internal_request(mock_request)

    self.assertEqual('expired',
                     str(cm.exception))

    mock_get_config_by_key_path.assert_called_once_with(['signing_secret'])

  @patch('shared_helpers.services.get_config_by_key_path', return_value='so_secret')
  def test_validate_internal_request__mismatched_url(self, mock_get_config_by_key_path):
    token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
                        'url': 'https://trot.to/api/users/1'},
                       'so_secret',
                       algorithm='HS256')

    mock_request = Mock()

    mock_request.headers = {'X-Token': token}
    mock_request.url = 'https://trot.to/api/users'

    with self.assertRaises(services.InvalidInternalToken) as cm:
      services.validate_internal_request(mock_request)

    self.assertEqual('mismatched URL',
                     str(cm.exception))

    mock_get_config_by_key_path.assert_called_once_with(['signing_secret'])

  @patch('shared_helpers.services.get_config_by_key_path', return_value='so_secret')
  def test_validate_internal_request__valid_token(self, mock_get_config_by_key_path):
    token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
                        'url': 'https://trot.to/api/users'},
                       'so_secret',
                       algorithm='HS256')

    mock_request = Mock()

    mock_request.headers = {'X-Token': token}
    mock_request.url = 'https://trot.to/api/users'

    self.assertEqual(True,
                     services.validate_internal_request(mock_request))

    mock_get_config_by_key_path.assert_called_once_with(['signing_secret'])


routes = Blueprint('test', __name__)


@routes.route('/_/api/users', methods=['GET'])
def get_users():
  services.validate_internal_request(request)

  return jsonify([{'id': 1}])


class TestIntegration(TrottoTestCase):

  blueprints_under_test = [routes]
  start_live_app = True
  live_app_config = {'sessions_secret': 'a_sessions_secret',
                     'signing_secret': 'so_secret',
                     'postgres': {'url': 'postgresql://admin:testing@/testing_trotto_core'}}

  @patch('shared_helpers.config.get_config', return_value={'services': {'my_service': {'signing_secret': 'so_secret',
                                                                                       'base_url': LIVE_APP_HOST}}})
  def test_internal_request__real_handler__valid_token(self, _):
    self.assertEqual([{'id': 1}],
                     services.get('my_service', '/_/api/users'))

  @patch('shared_helpers.config.get_config', return_value={'services': {'my_service': {'signing_secret': 'a_secret',
                                                                                       'base_url': LIVE_APP_HOST}}})
  def test_internal_request__real_handler__invalid_token(self, _):
    with self.assertRaises(HTTPError) as cm:
      self.assertEqual([{'id': 1}],
                       services.get('my_service', '/_/api/users'))

    self.assertEqual(500,
                     cm.exception.response.status_code)
