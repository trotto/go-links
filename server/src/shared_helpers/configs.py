import logging
import os

import yaml

from shared_helpers import env


CONFIGS_PARENT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config')


class MissingConfigError(Exception):
  pass


def get_secrets(error_if_missing=True):
  secrets_file_name = 'secrets.yaml'
  try:
    with open(os.path.join(CONFIGS_PARENT_DIR, secrets_file_name)) as secrets_file:
      secrets = yaml.load(secrets_file, Loader=yaml.SafeLoader)
  except IOError:
    if error_if_missing:
      raise

    secrets = {}

  return secrets


def get_organization_config(org_id):
  try:
    with open(os.path.join(CONFIGS_PARENT_DIR,
                           'prod' if env.current_env_is_production() else 'dev',
                           'organizations',
                           org_id + '.yaml')) as f:
      config = yaml.load(f, Loader=yaml.SafeLoader)
  except IOError:
    return {}

  return config


def get_config():
  try:
    with open(os.path.join(CONFIGS_PARENT_DIR,
                           'prod' if env.current_env_is_production() else 'dev',
                           'config.yaml')) as f:
      config = yaml.load(f, Loader=yaml.SafeLoader)
  except IOError:
    return {}

  return config


def get_path_to_oauth_secrets():
  production_path = os.path.join(os.path.dirname(__file__), '../config/client_secrets.json')

  if not os.path.isfile(production_path):
    if env.current_env_is_local():
      return os.path.join(os.path.dirname(__file__), '../local/client_secrets_local_only.json')
    else:
      raise MissingConfigError('Missing `config/client_secrets.json` in non-local environment')

  return production_path
