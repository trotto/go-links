import os


APP_ENGINE_PLATFORM_ID = 'app_engine'
DATASTORE_DATABASE_ID = 'cloud_datastore'


def get_platform():
  return os.getenv('PLATFORM', APP_ENGINE_PLATFORM_ID)


def get_database():
  return os.getenv('DATABASE', DATASTORE_DATABASE_ID)


def current_env_is_production():
  if get_platform() == APP_ENGINE_PLATFORM_ID:
    return os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/')

  return os.getenv('ENVIRONMENT') == 'prod'


def current_env_is_local():
  return os.getenv('ENVIRONMENT') == 'dev'
