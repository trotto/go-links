import ldclient
from ldclient import Context, LDClient, ContextBuilder
from ldclient.config import Config
from werkzeug.local import LocalProxy

from shared_helpers import config
from modules.data.abstract.users import User

class Provider:
  """
  Launch Darkly client wrapper

  Provides Launch Darkly feature flags if key was provided in app.yml
  Fallbacks to default_feature_flags if Launch Darkly was not set up
  """
  default_feature_flags: dict[str, bool] = {
    'new_frontend': False,
  }
  launchdarkly_initialized = False
  sdk_key: str

  def __init__(self, config_: dict) -> None:
    """
    Creates LDClient instanse

    Args:
      config_: config parsed from app.yml
    """
    self.sdk_key = config_.get('launchdarkly', {}).get('key', None)

    if not self.sdk_key:
      return

    ldclient.set_config(Config(self.sdk_key))

    if ldclient.get().is_initialized():
      self.launchdarkly_initialized = True

  def _get_context_builder(self, user: User) -> ContextBuilder:
    if not user:
      return Context.builder('anonymus-user').anonymous(True)
    elif user.organization and '@' not in user.organization:
      return Context.builder(str(user.id)).set('organization', user.organization)
    else:
      return Context.builder('any-user-key')

  def get(self, feature_flag_key: str, user: User = None) -> bool:
    """
    Gets value of specified feature flag

    Args:
      feature_flag_key: Key of feature flag
      user: Flask's user obj

    Returns:
      bool value of the feature flag
    """
    if not self.launchdarkly_initialized:
      return self.default_feature_flags.get(feature_flag_key, False)
    
    context = self._get_context_builder(user).build()
    return ldclient.get().variation(feature_flag_key, context, False)
      

provider = Provider(config.get_config())