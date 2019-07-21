from google.appengine.ext import ndb


class BaseModel(ndb.Model):
  created = ndb.DateTimeProperty(auto_now_add=True)
  modified = ndb.DateTimeProperty(auto_now=True)
  oid = ndb.ComputedProperty(lambda self: self.key.id() if self.key else None)
