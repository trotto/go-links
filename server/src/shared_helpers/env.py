import os


APP_ENGINE_PLATFORM_ID = 'app_engine'


def get_platform():
  return os.getenv('PLATFORM', APP_ENGINE_PLATFORM_ID)


def current_env_is_production():
  if get_platform() == APP_ENGINE_PLATFORM_ID:
    return os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/')

  return os.getenv('ENVIRONMENT') == 'prod'


def current_env_is_local():
  return os.getenv('ENVIRONMENT') in ['dev', 'test_env']
