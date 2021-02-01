from unittest import TestCase

from modules.base import errors


class TestFunctions(TestCase):

  def test_get_error_message_from_code__static_message(self):
    self.assertEqual('Your account has been disabled by an administrator.',
                     errors.get_error_message_from_code('account_disabled'))

  def test_get_error_message_from_code__auth_not_allowed__text_for_method_code(self):
    self.assertEqual('Your organization does not allow signin with Google.',
                     errors.get_error_message_from_code('auth_not_allowed-google'))

  def test_get_error_message_from_code__auth_not_allowed__no_text_for_method_code(self):
    self.assertEqual('Your organization does not allow signin with custom_auth.',
                     errors.get_error_message_from_code('auth_not_allowed-custom_auth'))

  def test_get_error_message_from_code__unknown_code(self):
    self.assertEqual(None,
                     errors.get_error_message_from_code('auth_not_allowed-custom_auth-extra'))

    self.assertEqual(None,
                     errors.get_error_message_from_code('unknown'))
