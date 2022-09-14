#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unittest

from mock import patch, call

from modules.data import get_models
from modules.links import helpers
from testing import TrottoTestCase
from modules.data.abstract.users import User


ShortLink = get_models('links').ShortLink


class TestUtilityFunctions(TrottoTestCase):

  def test__encode_ascii_incompatible_chars__many_query_params(self):
    self.assertEqual(
      'https://console.cloud.google.com/datastore/entities/query?project=great-project'
      '&organizationId=12321&ns=NS&kind=CoolKind&sortDir=DESCENDING&sortCol=created',
      helpers._encode_ascii_incompatible_chars(
        u'https://console.cloud.google.com/datastore/entities/query?project=great-project'
        u'&organizationId=12321&ns=NS&kind=CoolKind&sortDir=DESCENDING&sortCol=created'))

  def test__encode_ascii_incompatible_chars__empty_string_parameter_value(self):
    self.assertEqual(
      'https://console.cloud.google.com/datastore/entities/query'
      '?project=great-project&ns=&organizationId=12321',
      helpers._encode_ascii_incompatible_chars(u'https://console.cloud.google.com/datastore/entities/query'
                                               u'?project=great-project&ns=&organizationId=12321'))

  def test__encode_ascii_incompatible_chars__url_has_fragment(self):
    self.assertEqual(
      'https://trot.to/?section=getting-to-shortlinks#/how-it-works',
      helpers._encode_ascii_incompatible_chars(u'https://trot.to/?section=getting-to-shortlinks#/how-it-works'))

  def test__encode_ascii_incompatible_chars__percent_encoding_required(self):
    self.assertEqual(
      'https://github.com/search?utf8=%E2%9C%93&q=party+parrot&type=',
      helpers._encode_ascii_incompatible_chars(u'https://github.com/search?utf8=✓&q=party+parrot&type='))

  def test__encode_ascii_incompatible_chars__already_percent_encoded(self):
    self.assertEqual(
      'https://github.com/search?utf8=%E2%9C%93&q=party+parrot&type=',
      helpers._encode_ascii_incompatible_chars(u'https://github.com/search?utf8=%E2%9C%93&q=party+parrot&type='))

  def test__validate_destination__valid__simple(self):
    helpers._validate_destination('https://trot.to/getting-started')

  def test__validate_destination__valid__ip(self):
    helpers._validate_destination('http://142.251.33.14/search?q=trotto')

  def test__validate_destination__bare_hostname(self):
    helpers._validate_destination('http://go/directory')

    helpers._validate_destination('http://intranet:8000/directory')

    helpers._validate_destination('http://localhost:8000/directory')
    helpers._validate_destination('http://localhost/directory')
 
  def test__validate_destination__idn(self):
    helpers._validate_destination('https://double--hyphen.example.com/some/path')

    helpers._validate_destination('https://double--1-hyphen.example.com/other/path')
    
    helpers._validate_destination('https://triple-3---2--hyphen.example.com/other/path')

  def test__validate_destination__invalid(self):
    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers._validate_destination('http://>>/directory')

    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers._validate_destination('http://company directory')


def _get_user(user_email):
  return User(email=user_email)


class TestOtherFunctions(TrottoTestCase):

  def setUp(self):
    super().setUp()

    self._populate_test_links()

  def _populate_test_links(self):
    test_shortlinks = [

      # company2 - go/drive
      ShortLink(id=13,
                organization='2.com',
                owner='jay@2.com',
                namespace='go',
                shortpath='drive',
                shortpath_prefix='drive',
                destination_url='http://drive3.com'),

      # company1 - go/drive
      ShortLink(id=14,
                organization='1.com',
                owner='kay@1.com',
                namespace='go',
                shortpath='drive',
                shortpath_prefix='drive',
                destination_url='http://drive4.com'),

      # company2 - go/drive/%s
      ShortLink(id=15,
                organization='2.com',
                owner='jay@2.com',
                namespace='go',
                shortpath='drive/%s',
                shortpath_prefix='drive',
                destination_url='http://drive5.com/%s'),

      # company1 - go/drive/%s
      ShortLink(id=16,
                organization='1.com',
                owner='kay@1.com',
                namespace='go',
                shortpath='drive/%s',
                shortpath_prefix='drive',
                destination_url='http://drive6.com/%s'),

      # company2 - go/paper/%s
      ShortLink(id=114,
                organization='2.com',
                owner='jay@2.com',
                namespace='go',
                shortpath='paper/%s',
                shortpath_prefix='paper',
                destination_url='http://paper.com/%s'),

      # company1 - go/sfdc/%s
      ShortLink(id=115,
                organization='1.com',
                owner='jay@1.com',
                namespace='go',
                shortpath='sfdc/%s',
                shortpath_prefix='sfdc',
                destination_url='http://sfdc.com/%s'),

      # company1 - go/looker/%s/%s
      ShortLink(id=116,
                organization='1.com',
                owner='jay@1.com',
                namespace='go',
                shortpath='looker/%s/%s',
                shortpath_prefix='looker',
                destination_url='http://looker.com/%s/search/%s'),

      # company1 - eng/drive
      ShortLink(id=117,
                organization='1.com',
                owner='jay@1.com',
                namespace='eng',
                shortpath='drive',
                shortpath_prefix='drive',
                destination_url='https://1.drive.com/eng'),

      # company2 - eng/drive
      ShortLink(id=118,
                organization='2.com',
                owner='jay@2.com',
                namespace='eng',
                shortpath='drive',
                shortpath_prefix='drive',
                destination_url='https://2.drive.com/eng')
    ]

    for link in test_shortlinks:
      link.put()

  def test_derive_pattern_match__one_level_shortlink(self):
    self.assertEqual((None, None),
                     helpers.derive_pattern_match('1.com', True, 'go', 'notes'))

  def test_derive_pattern_match__same_shortlink_different_companies(self):
    self.assertEqual((ShortLink.get_by_id(15), 'http://drive5.com/roadmap'),
                     helpers.derive_pattern_match('2.com', True, 'go', 'drive/roadmap'))

    self.assertEqual((ShortLink.get_by_id(15), 'http://drive5.com/roadmap'),
                     helpers.derive_pattern_match('2.com', True, 'go', 'drive/roadmap'))

    self.assertEqual((ShortLink.get_by_id(16), 'http://drive6.com/roadmap'),
                     helpers.derive_pattern_match('1.com', True, 'go', 'drive/roadmap'))

    self.assertEqual((ShortLink.get_by_id(16), 'http://drive6.com/roadmap'),
                     helpers.derive_pattern_match('1.com', True, 'go', 'drive/roadmap'))

    self.assertEqual((None, None),
                     helpers.derive_pattern_match('3.com', True, 'go', 'drive/roadmap'))

  def test_derive_pattern_match__go_link_exists_for_one_company_but_not_other(self):
    self.assertEqual((None, None),
                     helpers.derive_pattern_match('1.com', True, 'go', 'paper/kpis'))

    self.assertEqual((ShortLink.get_by_id(114), 'http://paper.com/kpis'),
                     helpers.derive_pattern_match('2.com', True, 'go', 'paper/kpis'))

  def test_derive_pattern_match__multi_level_pattern(self):
    self.assertEqual((ShortLink.get_by_id(116), 'http://looker.com/1/search/sales'),
                     helpers.derive_pattern_match('1.com', True, 'go', 'looker/1/sales'))

    # no looker/%s shortlink exists:
    self.assertEqual((None, None),
                     helpers.derive_pattern_match('1.com', True, 'go', 'looker/sales'))

  def test_get_shortlink__link_does_not_exist(self):
    self.assertEqual((None, None),
                     helpers.get_shortlink('1.com', True, False, 'go', 'slack'))

  def test_get_shortlink__simple_go_link(self):
    self.assertEqual((ShortLink.get_by_id(14), 'http://drive4.com'),
                     helpers.get_shortlink('1.com', True, False, 'go', 'drive'))

  def test_get_shortlink__go_link_with_placeholder(self):
    self.assertEqual((ShortLink.get_by_id(116), 'http://looker.com/7/search/users'),
                     helpers.get_shortlink('1.com', True, False, 'go', 'looker/7/users'))

  def test_get_shortlink__same_shortlink_different_companies__alternate_namespace(self):
    self.assertEqual((ShortLink.get_by_id(117), 'https://1.drive.com/eng'),
                     helpers.get_shortlink('1.com', True, False, 'eng', 'drive'))

    self.assertEqual((ShortLink.get_by_id(118), 'https://2.drive.com/eng'),
                     helpers.get_shortlink('2.com', True, False, 'eng', 'drive'))

  @patch('modules.links.helpers.upsert_short_link', return_value='mock_return')
  def test_update_short_link(self, mock_upsert_short_link):
    shortlink = ShortLink.get_by_id(115)

    shortlink.destination_url = 'http://sfdc1000.com/%s'

    self.assertEqual('mock_return',
                     helpers.update_short_link(_get_user('jay@1.com'), shortlink))

    self.assertEqual(mock_upsert_short_link.call_args_list,
                     [call(_get_user('jay@1.com'), '1.com', 'jay@1.com', 'go', 'sfdc/%s', 'http://sfdc1000.com/%s', shortlink)])

  def test_create_shortlink__go_link_already_exists(self):
    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', 'drive', 'drive1000.com', 'simple')

    self.assertEqual('That go link already exists. go/drive points to http://drive4.com',
                     str(cm.exception))

  def test_create_shortlink__owner_does_not_match_org(self):
    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers.create_short_link(_get_user('kay@g.com'), '1.com', 'kay@g.com', 'go', 'drive', 'drive1000.com', 'simple')

    self.assertEqual("The go link's owner must be in the go link's organization",
                     str(cm.exception))

  def test_get_all_shortlinks_for_org(self):
    expected_shortlinks = [ShortLink.get_by_id(id) for id in [14, 16, 115, 116, 117]]

    self.assertEqual(sorted(expected_shortlinks, key=lambda link: link.id),
                     sorted(helpers.get_all_shortlinks_for_org('1.com'), key=lambda link: link.id))


class TestOtherFunctionsEmptyDatabase(TrottoTestCase):

  def assert_entity_attributes(self, expected_attributes, entity):
    actual_attributes = {attr_name: getattr(entity, attr_name) for attr_name in expected_attributes.keys()}

    self.assertEqual(expected_attributes,
                     actual_attributes)

  def test_create_shortlink__successful_go_link_creation(self):
    new_link = helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', 'there', 'example.com', 'simple')

    self.assert_entity_attributes({'organization': '1.com',
                                   'owner': 'kay@1.com',
                                   'namespace': 'go',
                                   'shortpath': 'there',
                                   'shortpath_prefix': 'there',
                                   'destination_url': 'http://example.com',
                                   'visits_count': None,
                                   'visits_count_last_updated': None},
                                  new_link)

  def test_create_shortlink__successful_go_link_creation_with_same_link_at_other_company(self):
    new_link = helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', 'paper/%s', 'paper2.com/search/%s', 'simple')

    self.assert_entity_attributes({'organization': '1.com',
                                   'owner': 'kay@1.com',
                                   'namespace': 'go',
                                   'shortpath': 'paper/%s',
                                   'shortpath_prefix': 'paper',
                                   'destination_url': 'http://paper2.com/search/%s',
                                   'visits_count': None,
                                   'visits_count_last_updated': None},
                                  new_link)

  def test_create_short_link__keyword_with_underscore__simple_validation(self):
    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', 'home_page', 'https://www.trot.to', 'simple')

    self.assertEqual(helpers.PATH_RESTRICTIONS_ERROR_SIMPLE,
                     str(cm.exception))

  def test_create_short_link__non_ascii_keyword__simple_validation(self):
    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', u'こんにちは', 'https://www.trot.to', 'simple')

    self.assertEqual(helpers.PATH_RESTRICTIONS_ERROR_SIMPLE,
                     str(cm.exception))

  def test_create_short_link__invalid_keyword__expanded_validation(self):
    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'gohan', 'homepage>', 'https://www.trot.to', 'expanded')

    self.assertEqual(helpers.PATH_RESTRICTIONS_ERROR_EXPANDED,
                     str(cm.exception))

  def test_create_short_link__keyword_with_underscore__expanded_validation(self):
    new_link = helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', 'home_page', 'https://www.trot.to', 'expanded')

    self.assert_entity_attributes({'organization': '1.com',
                                   'owner': 'kay@1.com',
                                   'namespace': 'go',
                                   'shortpath': 'home_page',
                                   'shortpath_prefix': 'home_page',
                                   'destination_url': 'https://www.trot.to',
                                   'visits_count': None,
                                   'visits_count_last_updated': None},
                                  new_link)

  def test_create_short_link__non_ascii_keyword__expanded_validation(self):
    new_link = helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', u'こんにちは', 'https://www.trot.to', 'expanded')

    self.assert_entity_attributes({'organization': '1.com',
                                   'owner': 'kay@1.com',
                                   'namespace': 'go',
                                   'shortpath': u'こんにちは',
                                   'shortpath_prefix': u'こんにちは',
                                   'destination_url': 'https://www.trot.to',
                                   'visits_count': None,
                                   'visits_count_last_updated': None},
                                  new_link)


class TestHierarchicalLinks(TrottoTestCase):
  def assert_entity_attributes(self, expected_attributes, entity):
    actual_attributes = {attr_name: getattr(entity, attr_name) for attr_name in expected_attributes.keys()}

    self.assertEqual(expected_attributes, actual_attributes)

  def setUp(self):
    super().setUp()

    ShortLink(id=16,
              organization='1.com',
              owner='kay@1.com',
              namespace='go',
              shortpath='trotto/docs',
              shortpath_prefix='trotto',
              destination_url='http://www.trot.to/docs'
              ).put()

    ShortLink(id=17,
              organization='1.com',
              owner='kay@1.com',
              namespace='go',
              shortpath='trotto/fr/t',
              shortpath_prefix='trotto',
              destination_url='http://fr.trot.to'
              ).put()

    ShortLink(id=18,
              organization='1.com',
              owner='jay@1.com',
              namespace='go',
              shortpath='drive/%s',
              shortpath_prefix='drive',
              destination_url='http://drive.com/%s'
              ).put()

    ShortLink(id=19,
              organization='1.com',
              owner='jay@1.com',
              namespace='go',
              shortpath='drive/aaa/%s',
              shortpath_prefix='drive',
              destination_url='http://drive.com/aaa/%s'
              ).put()

  def test_get_shortlink__hierarchical_link_exists(self):
    self.assertEqual((ShortLink.get_by_id(16), 'http://www.trot.to/docs'),
                     helpers.get_shortlink('1.com', True, False, 'go', 'trotto/docs'))

    self.assertEqual((ShortLink.get_by_id(17), 'http://fr.trot.to'),
                     helpers.get_shortlink('1.com', True, False, 'go', 'trotto/fr/t'))

  def test_get_shortlink__hierarchical_link_exists_in_other_org(self):
    self.assertEqual((None, None),
                     helpers.get_shortlink('2.com', True, False, 'go', 'trotto/docs'))

  def test_get_shortlink__hierarchical_link_does_not_exist(self):
    self.assertEqual((None, None),
                     helpers.get_shortlink('1.com', True, False, 'go', 'trotto/jots'))

  def test_get_shortlink__hierarchical_link_does_not_exist__subpath_exists(self):
    self.assertEqual((None, None),
                     helpers.get_shortlink('1.com', True, False, 'go', 'trotto'))

    self.assertEqual((None, None),
                     helpers.get_shortlink('1.com', True, False, 'go', 'trotto/fr'))

  def test_create_short_link__conflicting_programmatic_link(self):
    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', 'drive/recent', 'drive.com/recent', 'simple')

    self.assertEqual('A conflicting go link already exists. go/drive/%s points to http://drive.com/%s',
                     str(cm.exception))

  def test_create_short_link__conflicting_hierarchical_programmatic_link(self):
    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', 'drive/aaa/test', 'drive.com/aaa/test', 'simple')

    self.assertEqual('A conflicting go link already exists. go/drive/aaa/%s points to http://drive.com/aaa/%s',
                     str(cm.exception))

  def test_create_short_link__not_conflicting_hierarchical_programmatic_link(self):
    new_link = helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', 'drive/bbb/%s', 'drive.com/bbb/%s', 'simple')

    self.assert_entity_attributes({'organization': '1.com',
                                   'owner': 'kay@1.com',
                                   'namespace': 'go',
                                   'shortpath': 'drive/bbb/%s',
                                   'shortpath_prefix': 'drive',
                                   'destination_url': 'http://drive.com/bbb/%s',
                                   'visits_count': None,
                                   'visits_count_last_updated': None},
                                  new_link)

                    
  def test_create_short_link__conflicting_hierarchical_link(self):
    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', 'trotto/%s', 'https://www.trot.to/q=%s', 'simple')

    self.assertEqual('A conflicting go link already exists. go/trotto/docs points to http://www.trot.to/docs',
                     str(cm.exception))

  def test_create_short_link__non_placeholder_after_placeholder(self):
    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers.create_short_link(_get_user('kay@1.com'), '1.com', 'kay@1.com', 'go', 'trotto/%s/q', 'https://www.trot.to/q=%s', 'simple')

    self.assertEqual('After the first "%s" placeholder, you can only have additional placeholders',
                     str(cm.exception))
