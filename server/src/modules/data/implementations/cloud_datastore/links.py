import os

from google.cloud import datastore

from modules.data.abstract import links

datastore_client = datastore.Client()


SHORTLINK_KIND = 'ShortLink'


def _dict_to_object(link_dict):
  link_dict['id'] = link_dict.id
  return ShortLink(**link_dict)


class ShortLink(links.ShortLink):

  @staticmethod
  def get_by_id(id):
    match = datastore_client.get(datastore_client.key(SHORTLINK_KIND, int(id)))

    return _dict_to_object(match) if match else None

  @staticmethod
  def get_by_prefix(organization, shortpath_prefix):
    query = datastore_client.query(kind=SHORTLINK_KIND)

    query.add_filter('organization', '=', organization)
    query.add_filter('shortpath_prefix', '=', shortpath_prefix)

    return [_dict_to_object(link) for link in query.fetch()]

  @staticmethod
  def get_by_full_path(organization, shortpath):
    query = datastore_client.query(kind=SHORTLINK_KIND)

    query.add_filter('organization', '=', organization)
    query.add_filter('shortpath', '=', shortpath)

    matches = list(query.fetch())

    return _dict_to_object(matches[0]) if matches else None

  @staticmethod
  def get_by_organization(organization):
    query = datastore_client.query(kind=SHORTLINK_KIND)

    query.add_filter('organization', '=', organization)

    return [_dict_to_object(link) for link in query.fetch()]

  def put(self):
    super().put()

    if self.id:
      entity = datastore.Entity(key=datastore_client.key(SHORTLINK_KIND, self.id))
    else:
      entity = datastore.Entity(key=datastore_client.key(SHORTLINK_KIND))

    entity.update({k: getattr(self, k) for k in self._properties})

    datastore_client.put(entity)

    self.id = entity.id

  def delete(self):
    datastore_client.delete(datastore_client.key(SHORTLINK_KIND, self.id))

  @staticmethod
  def _get_all():
    if os.getenv('ENVIRONMENT') == 'test_env':
      query = datastore_client.query(kind=SHORTLINK_KIND)

      return [_dict_to_object(link) for link in query.fetch()]
