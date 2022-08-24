from urllib.parse import quote

from modules.data import get_models
from modules.organizations.utils import get_organization_id_for_email
from shared_helpers import config
from shared_helpers.encoding import convert_entity_to_dict
from shared_helpers.events import enqueue_event
from shared_helpers.services import get as service_get


models = get_models('users')

class LoginEmailException(Exception):
  pass


class LoginLinkValidationError(Exception):
  pass


def _extract_domain_type(email):
  return 'generic' if '@' in get_organization_id_for_email(email) else 'corporate'


def get_user_by_id(user_id):
  return models.User.get_by_id(user_id)


def get_users_by_organization(org_id):
  return models.User.query.filter(models.User.organization == org_id)


def get_or_create_user(email, user_org):
  email = email.lower()

  user = models.User.get_by_email_and_org(email, user_org)

  if not user:
    user = models.User(email=email,
                       organization=user_org,
                       domain_type=_extract_domain_type(email))
    user.put()

    enqueue_event(user.organization,
                  'user.created',
                  'user',
                  convert_entity_to_dict(user, ['id', 'email', 'organization']),
                  user=user)

  return user


def get_admin_ids(organization):
  try:
    return [user['id'] for user
            in service_get('admin', f'/organizations/{quote(organization)}/users?role=admin')]
  except config.ServiceNotConfiguredError:
    return None


def is_user_admin(user, organization=None):
  if organization and organization != user.organization:
    return False

  admin_ids = get_admin_ids(user.organization)
  if admin_ids is not None:
    return user.id in admin_ids

  org_config = config.get_organization_config(user.organization)

  return user.email in org_config.get('admins', []) if org_config else False
