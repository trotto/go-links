import unittest
from mock import patch

from modules.organizations import utils

class FunctionsTests(unittest.TestCase):

  @patch('shared_helpers.config.get_organization_config', return_value=None)
  def test_get_organization_id_for_email__corp_domain(self, mock_get_organization_config):
    self.assertEqual('optimizely.com',
                     utils.get_organization_id_for_email('alf@optimizely.com'))

    mock_get_organization_config.assert_called_once_with('optimizely.com')

  def test_get_organization_id_for_email__generic_domain(self):
    self.assertEqual('alex@gmail.com',
                     utils.get_organization_id_for_email('alex@gmail.com'))

  def test_get_organization_id_for_email__special_test_org(self):
    self.assertEqual('test_org',
                     utils.get_organization_id_for_email('itsotester1@gmail.com'))

  @patch('shared_helpers.config.get_organization_config', return_value={'alias_to': 'itso.io'})
  def test_get_organization_id_for_email__aliased_domain(self, mock_get_organization_config):
    self.assertEqual('itso.io',
                     utils.get_organization_id_for_email('alex@itso.co'))

    mock_get_organization_config.assert_called_once_with('itso.co')

  @patch('shared_helpers.config.get_organization_config', return_value={'alias_to': '1@gmail.com'})
  def test_get_organization_id_for_email__aliased_email_for_generic_provider(self, mock_get_organization_config):
    self.assertEqual('1@gmail.com',
                     utils.get_organization_id_for_email('2@gmail.com'))

    mock_get_organization_config.assert_called_once_with('2@gmail.com')
