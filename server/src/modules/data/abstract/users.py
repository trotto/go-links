from datetime import datetime

from modules.data.abstract.base import BaseModel
from modules.organizations.utils import get_organization_id_for_email


class User(BaseModel):
  email = str
  organization = str
  enabled = bool
  role = str
  accepted_terms_at = datetime
  domain_type = str
  notifications = dict

  is_authenticated = True  # as required by Flask-Login
  is_active = True  # as required by Flask-Login
  is_anonymous = False  # as required by Flask-Login

  # TODO: Eliminate the need for this duplication with a better base class.
  _properties = ['id', 'created', 'modified',
                 'email', 'organization', 'enabled', 'role', 'accepted_terms_at',
                 'domain_type', 'notifications']

  def __eq__(self, other):
    # simple comparison for unit tests
    return self.id == other.id if self.id else (self.email == other.email and self.organization == other.organization)

  def get_id(self):  # as required by Flask-Login
    return str(super().get_id())

  @staticmethod
  def get_by_email_and_org(email, org):
    raise NotImplementedError
