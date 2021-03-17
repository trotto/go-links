from urllib.parse import quote

from shared_helpers import config
from shared_helpers.services import get as service_get


def get_org_settings(organization):
  try:
    return service_get('admin', f'/organizations/{quote(organization)}/settings')
  except config.ServiceNotConfiguredError:
    return {}
