import os
import sys

import yaml

sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src'))
from shared_helpers.config import get_config
from shared_helpers.utils import generate_secret


def _write_secrets(updated_secrets):
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src/config/secrets.yaml'), 'w') as f:
    yaml.dump(updated_secrets, f, default_flow_style=False)

  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src/config/.set_env_vars'), 'w') as f:
    f.write('export TROTTO_APP_ID=%s' % (secrets['app_id']))


def _check_for_client_secrets():
  if not os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src/config/client_secrets.json')):
    print('\nTo deploy to App Engine, you must include a src/config/client_secrets.json. For guidance, see'
          ' https://github.com/trotto/go-links#obtain-oauth-client-credentials.')

    sys.exit(1)


if __name__ == "__main__":
  secrets = get_config(False) or {}

  if 'sessions_secret' not in secrets:
    user_input = raw_input("You don't yet have a sessions secret, so one will be created for you and stored"
                           " in src/config/secrets.yaml. Be sure to store this secret somewhere safe."
                           " Hit Enter to continue. ")
    print('\n')

    secrets['sessions_secret'] = generate_secret(64)

  if 'app_id' not in secrets:
    secrets['app_id'] = raw_input("What's your App Engine app ID? ")

  _write_secrets(secrets)

  _check_for_client_secrets()

  os.environ['TROTTO_APP_ID'] = secrets['app_id']
