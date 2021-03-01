import datetime

from mock import patch

from modules.data.implementations.postgres import links

from testing import TrottoTestCase


class TestFunctions(TrottoTestCase):

  def test__get_link_key__go_namespace(self):
    self.assertEqual("b'Z29vZ3MuY29t':roadmap",
                     links._get_link_key('googs.com', 'go', 'roadmap'))

  def test__get_link_key__no_namespace(self):
    self.assertEqual("b'Z29vZ3MuY29t':roadmap",
                     links._get_link_key('googs.com', None, 'roadmap'))

  def test__get_link_key__other_namespace(self):
    self.assertEqual("b'Z29vZ3MuY29t':eng:roadmap",
                     links._get_link_key('googs.com', 'eng', 'roadmap'))

  def test__get_link_key__complex_path(self):
    self.assertEqual("b'Z29vZ3MuY29t':eng:roadmap/q2",
                     links._get_link_key('googs.com', 'eng', 'roadmap/q2'))

  def _add_link(self, namespace, path, organization='googs.com'):
    link = links.ShortLink(created=datetime.datetime(2018, 10, 1),
                           organization=organization,
                           owner=f'kay@{organization}',
                           namespace=namespace,
                           shortpath=path,
                           shortpath_prefix=path.split('/')[0],
                           destination_url='http://example.com')

    link.put()

    return link

  def test_put__go_namespace(self):
    self._add_link('go', 'there')

    self.assertEqual([None],
                     [l._ns for l in links.ShortLink._get_all()])

  def test_put__ns_column_explicitly_set_to_go(self):
    links.ShortLink(created=datetime.datetime(2018, 10, 1),
                    organization='googs.com',
                    owner=f'kay@googs.com',
                    namespace='go',
                    _ns='go',
                    shortpath='there',
                    shortpath_prefix='there',
                    destination_url='http://example.com'
                    ).put()

    self.assertEqual([None],
                     [l._ns for l in links.ShortLink._get_all()])

  @patch('modules.data.implementations.postgres.links.get_default_namespace', return_value='yo')
  def test_put__ns_column_explicitly_set_to_alternative_default_namespace(self, mock_get_default_namespace):
    links.ShortLink(created=datetime.datetime(2018, 10, 1),
                    organization='googs.com',
                    owner=f'kay@googs.com',
                    namespace='yo',
                    _ns='yo',
                    shortpath='there',
                    shortpath_prefix='there',
                    destination_url='http://example.com'
                    ).put()

    self.assertEqual([None],
                     [l._ns for l in links.ShortLink._get_all()])

    mock_get_default_namespace.assert_called_with('googs.com')

  def test_put__other_namespace(self):
    self._add_link('eng', 'there')

    self.assertEqual(['eng'],
                     [l._ns for l in links.ShortLink._get_all()])

  @patch('modules.data.implementations.postgres.links.get_default_namespace', return_value='eng')
  def test_put__alternative_default_namespace(self, mock_get_default_namespace):
    self._add_link('eng', 'there')

    self.assertEqual([None],
                     [l._ns for l in links.ShortLink._get_all()])

    mock_get_default_namespace.assert_called_with('googs.com')

  def test_get_by_id__go_namespace(self):
    go_link = self._add_link('go', '1')
    go_link = links.ShortLink.get_by_id(go_link.get_id())

    self.assertEqual("b'Z29vZ3MuY29t':1",
                     go_link.key)
    self.assertEqual('go',
                     go_link.namespace)

  def test_get_by_id__other_namespace(self):
    eng_link = self._add_link('eng', '2')
    eng_link = links.ShortLink.get_by_id(eng_link.get_id())

    self.assertEqual("b'Z29vZ3MuY29t':eng:2",
                     eng_link.key)
    self.assertEqual('eng',
                     eng_link.namespace)

  def test_get_by_prefix(self):
    googs_link_1 = self._add_link('go', '1')
    googs_link_2 = self._add_link('go', '1/2')
    self._add_link('go', '2')
    self._add_link('eng', '1')
    self._add_link('go', '2', 'other.co')
    other_co_link = self._add_link('eng', '2', 'other.co')

    googs_links = links.ShortLink.get_by_prefix('googs.com', 'go', '1')
    googs_links = sorted(googs_links, key=lambda l: l.created)

    self.assertEqual([googs_link_1, googs_link_2], googs_links)
    # verify setting of non-column `namespace` prop
    self.assertEqual(['go', 'go'],
                     [l.namespace for l in googs_links])

    other_co_links = links.ShortLink.get_by_prefix('other.co', 'eng', '2')

    self.assertEqual([other_co_link], other_co_links)
    self.assertEqual('eng',
                     other_co_links[0].namespace)

  def test_get_by_full_path__go_namespace(self):
    self._add_link('go', '1')
    googs_link = self._add_link('go', '1/2')
    self._add_link('eng', '1/2')
    self._add_link('go', '1/2', 'other.co')

    queried_link = links.ShortLink.get_by_full_path('googs.com', 'go', '1/2')

    self.assertEqual(googs_link, queried_link)
    self.assertEqual('go',
                     queried_link.namespace)

  def test_get_by_full_path__other_namespace(self):
    self._add_link('go', '1')
    self._add_link('go', '1/2')
    googs_link = self._add_link('eng', '1/2')
    self._add_link('eng', '1/2', 'other.co')

    queried_link = links.ShortLink.get_by_full_path('googs.com', 'eng', '1/2')

    self.assertEqual(googs_link, queried_link)
    self.assertEqual('eng',
                     queried_link.namespace)

  def test_get_by_organization(self):
    link1 = self._add_link('go', '1')
    self._add_link('go', '1/2', 'other.co')
    link2 = self._add_link('eng', '1/2')

    googs_links = links.ShortLink.get_by_organization('googs.com')
    googs_links = sorted(googs_links, key=lambda l: l.created)

    self.assertEqual([link1, link2], googs_links)
    self.assertEqual(['go', 'eng'],
                      [l.namespace for l in googs_links])
