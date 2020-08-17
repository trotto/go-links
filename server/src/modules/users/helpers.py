import os

import jinja2

from modules.data import get_models
from modules.organizations.utils import get_organization_id_for_email
from shared_helpers import config
from shared_helpers.encoding import convert_entity_to_dict
from shared_helpers.events import enqueue_event


models = get_models('users')


JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../../static/templates')),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)


class LoginEmailException(Exception):
  pass


class LoginLinkValidationError(Exception):
  pass


def _extract_domain_type(email):
  return 'generic' if '@' in get_organization_id_for_email(email) else 'corporate'


def get_user_by_id(user_id):
  return models.User.get_by_id(user_id)


def get_or_create_user(email, user_org):
  email = email.lower()

  user = models.User.get_by_email(email)

  # TODO: Remove this when all users are backfilled
  if user and (not user.domain_type
               or not user.organization):
    user.domain_type = _extract_domain_type(email)

    if not user.organization:
      user.organization = user.extract_organization()

    user.put()

  if not user:
    user = models.User(email=email,
                       domain_type=_extract_domain_type(email))
    user.organization = user.extract_organization()
    user.put()

    enqueue_event('user.created',
                  'user',
                  convert_entity_to_dict(user, ['id', 'email', 'organization']))

  return user


def is_user_admin(user):
  org_config = config.get_organization_config(user.organization)

  return user.email in org_config.get('admins', []) if org_config else False
