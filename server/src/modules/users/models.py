from google.appengine.ext import ndb

from modules.base.models import BaseModel
from modules.organizations.utils import get_organization_id_for_email


class User(BaseModel):

  def extract_organization(self):
    return get_organization_id_for_email(self.email) if self.email else None

  def get_organization_name(self):
    return get_organization_id_for_email(self.email) if self.email else None

  email = ndb.StringProperty(required=True)
  organization = ndb.StringProperty()
  role = ndb.StringProperty(choices=['implementer'])
  accepted_terms_at = ndb.DateTimeProperty()
  domain_type = ndb.StringProperty(choices=['generic', 'corporate'])
  notifications = ndb.JsonProperty(default={})


class EmailLoginLink(BaseModel):
  email = ndb.StringProperty(required=True)
  secret = ndb.StringProperty(required=True)
  used = ndb.BooleanProperty(default=False)
