import urllib

from google.appengine.ext import ndb

from modules.base.models import BaseModel


class ShortLink(BaseModel):
  organization = ndb.StringProperty(required=True)
  owner = ndb.StringProperty(required=True)
  shortpath = ndb.StringProperty(required=True)
  # TODO: Make shortpath_prefix a computed property.
  shortpath_prefix = ndb.StringProperty()  # first part of path; for doing quick search for templates
  destination_url = ndb.StringProperty(required=True)
  visits_count = ndb.IntegerProperty()
  visits_count_last_updated = ndb.DateTimeProperty()
