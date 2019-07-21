import os

import yaml

import env


CONFIGS_PARENT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config')


def get_secrets(error_if_missing=True):
  secrets_file_name = 'secrets.yaml'
  try:
    with open(os.path.join(CONFIGS_PARENT_DIR, secrets_file_name)) as secrets_file:
      secrets = yaml.load(secrets_file)
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
      config = yaml.load(f)
  except IOError:
    return {}

  return config


def get_config():
  try:
    with open(os.path.join(CONFIGS_PARENT_DIR,
                           'prod' if env.current_env_is_production() else 'dev',
                           'config.yaml')) as f:
      config = yaml.load(f)
  except IOError:
    return {}

  return config
