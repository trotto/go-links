from urllib.parse import quote

from shared_helpers import config
from shared_helpers.services import get as service_get


def get_org_settings(organization):
  try:
    return service_get('admin', f'/organizations/{quote(organization)}/settings')
  except config.ServiceNotConfiguredError:
    return {}


def get_org_edit_mode(org_id):
  return get_org_settings(org_id).get('edit_mode', 'owners_and_admins_only')
