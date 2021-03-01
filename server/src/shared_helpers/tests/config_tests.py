import unittest

from mock import patch, mock_open

from shared_helpers import config


class TestFunctions(unittest.TestCase):

  @patch('os.path.isfile', return_value=True)
  def test_get_path_to_oauth_secrets__production_file_exists(self, mock_isfile):
    self.assertEqual('config/client_secrets.json',
                     '/'.join(config.get_path_to_oauth_secrets().rsplit('/', 2)[-2:]))

    self.assertTrue(mock_isfile.call_args[0][0].endswith('config/client_secrets.json'))

  @patch('shared_helpers.env.current_env_is_local', return_value=True)
  @patch('os.path.isfile', return_value=False)
  def test_get_path_to_oauth_secrets__production_file_does_not_exist__local_env(self, mock_isfile, mock_is_local):
    self.assertEqual('local/client_secrets_local_only.json',
                     '/'.join(config.get_path_to_oauth_secrets().rsplit('/', 2)[-2:]))

  @patch('shared_helpers.env.current_env_is_local', return_value=False)
  @patch('os.path.isfile', return_value=False)
  def test_get_path_to_oauth_secrets__production_file_does_not_exist__non_local_env(self, mock_isfile, mock_is_local):
    self.assertRaises(config.MissingConfigError, config.get_path_to_oauth_secrets)

  @patch('yaml.load', return_value={'mock': 'config'})
  @patch('os.path.isfile', return_value=True)
  @patch('os.getenv', return_value=None)
  def test_get_config__config_from_secrets_yaml_file(self, _0, _1, _2):
    with patch('builtins.open', mock_open(read_data='')) as mocked_open:
      self.assertEqual({'mock': 'config'},
                       config.get_config())

      self.assertTrue(mocked_open.call_args[0][0].endswith('secrets.yaml'))

  @patch('yaml.load', return_value={'mock': 'config'})
  @patch('os.path.isfile', side_effect=lambda path: path.endswith('app.yml'))
  @patch('os.getenv', return_value=None)
  def test_get_config__config_from_app_yml_file(self, _0, mock_is_file, _2):
    with patch('builtins.open', mock_open(read_data='')) as mocked_open:
      self.assertEqual({'mock': 'config'},
                       config.get_config())

      self.assertTrue(mocked_open.call_args[0][0].endswith('app.yml'))
      self.assertEqual(1, len(mock_is_file.call_args_list))
      self.assertTrue(mock_is_file.call_args[0][0].endswith('secrets.yaml'))

  @patch('os.path.isfile', return_value=False)
  def test_get_config__config_from_multiple_env_vars(self, _):
    def get_env(var_name):
      return {'TROTTO_CONFIG': None,
              'DATABASE_URL': 'pg_url',
              'FLASK_SECRET': 'the_secret'
              }[var_name]

    with patch('os.getenv', side_effect=get_env):
      self.assertEqual({'postgres': {'url': 'pg_url'},
                        'sessions_secret': 'the_secret'},
                       config.get_config())

  @patch('os.path.isfile', return_value=False)
  def test_get_config__config_from_single_env_var(self, _):
    def get_env(var_name):
      return {'TROTTO_CONFIG': 'YTogMQpiOiAy',
              'DATABASE_URL': 'pg_url',
              'FLASK_SECRET': 'the_secret'
              }[var_name]

    with patch('os.getenv', side_effect=get_env):
      self.assertEqual({'a': 1, 'b': 2},
                       config.get_config())

  def test_get_organization_config__from_dedicated_file(self):
    with patch('builtins.open', mock_open(read_data='admins:\n - sam@googs.com')) as mocked_open:
      self.assertEqual({'admins': ['sam@googs.com']},
                       config.get_organization_config('googs.com'))

      self.assertTrue(mocked_open.call_args[0][0].endswith('googs.com.yaml'))

  @patch('shared_helpers.config.get_config', return_value={'sessions_secret': 'secret', 'admins': ['sam@googsetc.com']})
  def test_get_organization_config__from_general_config_file(self, _):
    self.assertEqual({'admins': ['sam@googsetc.com']},
                     config.get_organization_config('googsetc.com'))

  @patch('shared_helpers.config.get_config', return_value={'sessions_secret': 'secret'})
  def test_get_organization_config__from_general_config_file__no_org_config(self, _):
    self.assertEqual({},
                     config.get_organization_config('googsetc.com'))

  @patch('shared_helpers.config.get_config', return_value={'default_namespace': 'gogogo'})
  @patch('shared_helpers.config.get_organization_config', return_value={'default_namespace': 'yo'})
  def test_get_default_namespace__set_at_org_level(self, mock_get_organization_config, _):
    self.assertEqual('yo',
                     config.get_default_namespace('googs.com'))

    mock_get_organization_config.assert_called_once_with('googs.com')

  @patch('shared_helpers.config.get_config', return_value={'default_namespace': 'gogogo'})
  @patch('shared_helpers.config.get_organization_config', return_value={})
  def test_get_default_namespace__only_set_at_app_level(self, mock_get_organization_config, _):
    self.assertEqual('gogogo',
                     config.get_default_namespace('googs.com'))

    mock_get_organization_config.assert_called_once_with('googs.com')

  @patch('shared_helpers.config.get_config', return_value={})
  @patch('shared_helpers.config.get_organization_config', return_value={})
  def test_get_default_namespace__not_set(self, mock_get_organization_config, _):
    self.assertEqual('go',
                     config.get_default_namespace('googs.com'))

    mock_get_organization_config.assert_called_once_with('googs.com')
