from modules.users.constants import GENERIC_EMAIL_DOMAINS
from shared_helpers import configs
from shared_helpers.constants import TEST_ORGANIZATION_EMAIL_ADDRESSES, TEST_ORGANIZATION_ID


def get_organization_id_for_email(email_address):
  if email_address in TEST_ORGANIZATION_EMAIL_ADDRESSES:
    return TEST_ORGANIZATION_ID

  email_domain = email_address.split('@')[1].strip()
  if email_domain in GENERIC_EMAIL_DOMAINS:
    # links for generic emails are siloed to just that email
    return email_address.strip()

  org_config = configs.get_organization_config(email_domain)

  return org_config.get('alias_to', email_domain) if org_config else email_domain
