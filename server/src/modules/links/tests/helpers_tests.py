#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unittest

from mock import patch, call

from modules.data import get_models
from modules.links import helpers
from testing import TrottoTestCase


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
                shortpath='drive',
                shortpath_prefix='drive',
                destination_url='http://drive3.com'),

      # company1 - go/drive
      ShortLink(id=14,
                organization='1.com',
                owner='kay@1.com',
                shortpath='drive',
                shortpath_prefix='drive',
                destination_url='http://drive4.com'),

      # company2 - go/drive/%s
      ShortLink(id=15,
                organization='2.com',
                owner='jay@2.com',
                shortpath='drive/%s',
                shortpath_prefix='drive',
                destination_url='http://drive5.com/%s'),

      # company1 - go/drive/%s
      ShortLink(id=16,
                organization='1.com',
                owner='kay@1.com',
                shortpath='drive/%s',
                shortpath_prefix='drive',
                destination_url='http://drive6.com/%s'),

      # company2 - go/paper/%s
      ShortLink(id=114,
                organization='2.com',
                owner='jay@2.com',
                shortpath='paper/%s',
                shortpath_prefix='paper',
                destination_url='http://paper.com/%s'),

      # company1 - go/sfdc/%s
      ShortLink(id=115,
                organization='1.com',
                owner='jay@1.com',
                shortpath='sfdc/%s',
                shortpath_prefix='sfdc',
                destination_url='http://sfdc.com/%s'),

      # company1 - go/looker/%s/%s
      ShortLink(id=116,
                organization='1.com',
                owner='jay@1.com',
                shortpath='looker/%s/%s',
                shortpath_prefix='looker',
                destination_url='http://looker.com/%s/search/%s'),
    ]

    for link in test_shortlinks:
      link.put()

  def test_derive_pattern_match__one_level_shortlink(self):
    self.assertEqual((None, None),
                     helpers.derive_pattern_match('1.com', 'notes'))

  def test_derive_pattern_match__same_shortlink_different_companies(self):
    self.assertEqual((ShortLink.get_by_id(15), 'http://drive5.com/roadmap'),
                     helpers.derive_pattern_match('2.com', 'drive/roadmap'))

    self.assertEqual((ShortLink.get_by_id(15), 'http://drive5.com/roadmap'),
                     helpers.derive_pattern_match('2.com', 'drive/roadmap'))

    self.assertEqual((ShortLink.get_by_id(16), 'http://drive6.com/roadmap'),
                     helpers.derive_pattern_match('1.com', 'drive/roadmap'))

    self.assertEqual((ShortLink.get_by_id(16), 'http://drive6.com/roadmap'),
                     helpers.derive_pattern_match('1.com', 'drive/roadmap'))

    self.assertEqual((None, None),
                     helpers.derive_pattern_match('3.com', 'drive/roadmap'))

  def test_derive_pattern_match__go_link_exists_for_one_company_but_not_other(self):
    self.assertEqual((None, None),
                     helpers.derive_pattern_match('1.com', 'paper/kpis'))

    self.assertEqual((ShortLink.get_by_id(114), 'http://paper.com/kpis'),
                     helpers.derive_pattern_match('2.com', 'paper/kpis'))
  def test_derive_pattern_match__multi_level_pattern(self):
    self.assertEqual((ShortLink.get_by_id(116), 'http://looker.com/1/search/sales'),
                     helpers.derive_pattern_match('1.com', 'looker/1/sales'))

    # no looker/%s shortlink exists:
    self.assertEqual((None, None),
                     helpers.derive_pattern_match('1.com', 'looker/sales'))

  def test_get_shortlink__link_does_not_exist(self):
    self.assertEqual((None, None),
                     helpers.get_shortlink('1.com', 'slack'))

  def test_get_shortlink__simple_go_link(self):
    self.assertEqual((ShortLink.get_by_id(14), 'http://drive4.com'),
                     helpers.get_shortlink('1.com', 'drive'))

  def test_get_shortlink__go_link_with_placeholder(self):
    self.assertEqual((ShortLink.get_by_id(116), 'http://looker.com/7/search/users'),
                     helpers.get_shortlink('1.com', 'looker/7/users'))

  def assert_entity_attributes(self, expected_attributes, entity):
    actual_attributes = {attr_name: getattr(entity, attr_name) for attr_name in expected_attributes.keys()}

    self.assertEqual(expected_attributes,
                     actual_attributes)

  def test_create_shortlink__successful_go_link_creation(self):
    new_link = helpers.create_short_link('1.com', 'kay@1.com', 'there', 'example.com')

    self.assert_entity_attributes({'organization': '1.com',
                                   'owner': 'kay@1.com',
                                   'shortpath': 'there',
                                   'shortpath_prefix': 'there',
                                   'destination_url': 'http://example.com',
                                   'visits_count': None,
                                   'visits_count_last_updated': None},
                                  new_link)

  @patch('modules.links.helpers.upsert_short_link', return_value='mock_return')
  def test_update_short_link(self, mock_upsert_short_link):
    shortlink = ShortLink.get_by_id(115)

    shortlink.destination_url = 'http://sfdc1000.com/%s'

    self.assertEqual('mock_return',
                     helpers.update_short_link(shortlink))

    self.assertEqual(mock_upsert_short_link.call_args_list,
                     [call('1.com', 'jay@1.com', 'sfdc/%s', 'http://sfdc1000.com/%s', shortlink)])

  def test_create_shortlink__go_link_already_exists(self):
    with self.assertRaises(helpers.LinkCreationException) as cm:
      helpers.create_short_link('1.com', 'kay@1.com', 'drive', 'drive1000.com')

    self.assertEqual('That go link already exists. go/drive points to http://drive4.com',
                     str(cm.exception))

  def test_create_shortlink__successful_go_link_creation_with_same_link_at_other_company(self):
    new_link = helpers.create_short_link('1.com', 'kay@1.com', 'paper/%s', 'paper2.com/search/%s')

    self.assert_entity_attributes({'organization': '1.com',
                                   'owner': 'kay@1.com',
                                   'shortpath': 'paper/%s',
                                   'shortpath_prefix': 'paper',
                                   'destination_url': 'http://paper2.com/search/%s',
                                   'visits_count': None,
                                   'visits_count_last_updated': None},
                                  new_link)

  def test_get_all_shortlinks_for_org(self):
    ids_of_expected_shortlinks = [14, 16, 115, 116]

    expected_shortlinks = [ShortLink.get_by_id(id) for id in ids_of_expected_shortlinks]

    self.assertEqual(sorted(expected_shortlinks, key=lambda link: link.id),
                     sorted(helpers.get_all_shortlinks_for_org('1.com'), key=lambda link: link.id))
