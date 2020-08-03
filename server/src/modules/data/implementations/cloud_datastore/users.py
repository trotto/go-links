from google.cloud import datastore

from modules.data.abstract import users

datastore_client = datastore.Client()


USER_KIND = 'User'


def _dict_to_object(user_dict):
  user_dict['id'] = user_dict.id
  return User(**user_dict)


class User(users.User):

  @staticmethod
  def get_by_id(id):
    match = datastore_client.get(datastore_client.key(USER_KIND, int(id)))

    return _dict_to_object(match) if match else None

  @staticmethod
  def get_by_email(email):
    query = datastore_client.query(kind=USER_KIND)

    query.add_filter('email', '=', email)

    matches = list(query.fetch())

    return _dict_to_object(matches[0]) if matches else None

  def put(self):
    super().put()

    if self.id:
      entity = datastore.Entity(key=datastore_client.key(USER_KIND, self.id))
    else:
      entity = datastore.Entity(key=datastore_client.key(USER_KIND))

    entity.update({k: getattr(self, k) for k in self._properties})

    datastore_client.put(entity)

    self.id = entity.id
    self.oid = entity.id
