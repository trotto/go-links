from mock import Mock

from modules.base import authentication
from testing import TrottoTestCase


class TestFunctions(TrottoTestCase):

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
