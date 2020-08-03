from datetime import datetime

from modules.data.abstract.base import BaseModel
from modules.organizations.utils import get_organization_id_for_email


class User(BaseModel):
  email = str
  organization = str
  role = str
  accepted_terms_at = datetime
  domain_type = str
  notifications = dict

  # TODO: Eliminate the need for this duplication with a better base class.
  _properties = ['id', 'oid', 'created', 'modified',
                 'email', 'organization', 'role', 'accepted_terms_at',
                 'domain_type', 'notifications']

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.is_authenticated = True  # as required by Flask-Login
    self.is_active = True  # as required by Flask-Login
    self.is_anonymous = False  # as required by Flask-Login

    self.organization = get_organization_id_for_email(kwargs['email'])

  def get_id(self):  # as required by Flask-Login
    return str(super().get_id())

  def extract_organization(self):
    return get_organization_id_for_email(self.email) if self.email else None

  @staticmethod
  def get_by_email(email):
    raise NotImplementedError
