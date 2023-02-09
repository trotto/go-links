import ldclient
from ldclient import Context, LDClient
from ldclient.config import Config
from werkzeug.local import LocalProxy

from shared_helpers import config

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

  def get(self, feature_flag_key: str, user: LocalProxy = None) -> bool:
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

    has_organization = user and user.organization and '@' not in user.organization

    context = Context.builder(user.id) \
      .set('organization', user.organization) \
      .build() if has_organization else Context.builder('any-user-key').build()
    return ldclient.get().variation(feature_flag_key, context, False)
      

provider = Provider(config.get_config())