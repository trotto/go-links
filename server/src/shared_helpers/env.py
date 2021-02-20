import os


def current_env_is_local():
  return os.getenv('ENVIRONMENT') in ['dev', 'test_env']
