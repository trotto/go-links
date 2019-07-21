import os


def current_env_is_production():
  return os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/')


def current_env_is_local():
  return not current_env_is_production()
