from modules.users.constants import GENERIC_EMAIL_DOMAINS
from shared_helpers import config
from shared_helpers.constants import TEST_ORGANIZATION_EMAIL_ADDRESSES, TEST_ORGANIZATION_ID


def get_organization_id_for_email(email_address):
  if email_address in TEST_ORGANIZATION_EMAIL_ADDRESSES:
    return TEST_ORGANIZATION_ID

  email_domain = email_address.split('@')[1].strip()
  if email_domain in GENERIC_EMAIL_DOMAINS:
    # links for generic emails are siloed to just that email
    default_org = email_address.strip()
  else:
    default_org = email_domain

  org_config = config.get_organization_config(default_org)

  return org_config.get('alias_to', default_org) if org_config else default_org
