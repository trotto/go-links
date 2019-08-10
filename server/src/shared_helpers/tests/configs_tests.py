import unittest

from mock import patch, call

from shared_helpers import configs


class TestFunctions(unittest.TestCase):

  @patch('os.path.isfile', return_value=True)
  def test_get_path_to_oauth_secrets__production_file_exists(self, mock_isfile):
    self.assertEqual('config/client_secrets.json',
                     '/'.join(configs.get_path_to_oauth_secrets().rsplit('/', 2)[-2:]))

    self.assertTrue(mock_isfile.call_args[0][0].endswith('config/client_secrets.json'))

  @patch('shared_helpers.env.current_env_is_local', return_value=True)
  @patch('os.path.isfile', return_value=False)
  def test_get_path_to_oauth_secrets__production_file_does_not_exist__local_env(self, mock_isfile, mock_is_local):
    self.assertEqual('local/client_secrets_local_only.json',
                     '/'.join(configs.get_path_to_oauth_secrets().rsplit('/', 2)[-2:]))

  @patch('shared_helpers.env.current_env_is_local', return_value=False)
  @patch('os.path.isfile', return_value=False)
  def test_get_path_to_oauth_secrets__production_file_does_not_exist__non_local_env(self, mock_isfile, mock_is_local):
    self.assertRaises(configs.MissingConfigError, configs.get_path_to_oauth_secrets)
