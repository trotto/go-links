import unittest

from mock import patch, mock_open

from shared_helpers import feature_flags

class LDCMock:
  def __init__(self, is_initialized: bool = True, flag_value: bool = True):
    self._is_initialized = is_initialized
    self._flag_value = flag_value

  def is_initialized(self) -> bool:
    return self._is_initialized

  def variation(self, *args, **kwargs) -> bool:
    return self._flag_value


class TestFunctions(unittest.TestCase):

  @patch('ldclient.Context.builder')
  @patch('ldclient.get', return_value=LDCMock())
  def test_get_via_ld(self, ldc_mock, context_builder):
    class UserMock:
      id = 'user_id'
      organization = 'organization'

    config = {
      'launchdarkly': {
        'key': 'key'
      }
    }
    provider = feature_flags.Provider(config)
    self.assertEqual(provider.sdk_key, config['launchdarkly']['key'])
    self.assertEqual(provider.launchdarkly_initialized, True)

    user = UserMock()
    self.assertEqual(provider.get('new_frontend', user), True)
    context_builder.assert_called_once_with(user.id)

  @patch('ldclient.Context.builder')
  @patch('ldclient.get', return_value=LDCMock(flag_value=False))
  def test_get_via_ld_without_user(self, ldc_mock, context_builder):
    config = {
      'launchdarkly': {
        'key': 'key'
      }
    }
    provider = feature_flags.Provider(config)

    self.assertEqual(provider.get('new_frontend'), False)
    context_builder.assert_called_once_with('anonymus-user')


  def test_get_without_ld(self):
    config = {}
    provider = feature_flags.Provider(config)
    self.assertEqual(provider.sdk_key, None)
    self.assertEqual(provider.launchdarkly_initialized, False)

    """will get default values if launchdarky is not set up"""
    self.assertEqual(provider.get('new_frontend'), False)
    provider.default_feature_flags['new_frontend'] = True
    self.assertEqual(provider.get('new_frontend'), True)

    """will fallback to False if default flag is not set up"""
    self.assertEqual(provider.get('unknown_flag'), False)

  @patch('ldclient.get', return_value=LDCMock(is_initialized=False))
  def test_get_with_uninitialized_ld(self, ldc_mock):
    config = {
      'launchdarkly': {
        'key': 'key'
      }
    }
    provider = feature_flags.Provider(config)
    self.assertEqual(provider.sdk_key, config['launchdarkly']['key'])
    self.assertEqual(provider.launchdarkly_initialized, False)

    """will fallback to default values"""
    self.assertEqual(provider.get('new_frontend'), False)
    self.assertEqual(provider.get('unknown_flag'), False)


  @patch('ldclient.Context.builder')
  @patch('ldclient.get', return_value=LDCMock())
  def test_get_global_ld_flag_for_personal_user(self, ldc_mock, context_builder):
    class UserMock:
      id = 'user_id'
      organization = 'personal@ema.il'

    config = {
      'launchdarkly': {
        'key': 'key'
      }
    }
    provider = feature_flags.Provider(config)

    user = UserMock()
    self.assertEqual(provider.get('new_frontend', user), True)
    context_builder.assert_called_once_with('any-user-key')
