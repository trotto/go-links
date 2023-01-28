import ldclient
from ldclient import Context
from ldclient.config import Config

from shared_helpers import config

class Provider:
  default_feature_flag: dict[str, bool] = {
    'new_frontend': False,
  }
  launchdarky_initialized = False

  def __init__(self, config_: dict):

    self.sdk_key = config_.get('launchdarky', {}).get('key', None)
  
    if not self.sdk_key:
      return

    self.ldclient = ldclient.set_config(Config(self.sdk_key))

    if not ldclient.get().is_initialized():
      return

    self.launchdarky_initialized = True
    self.context = Context.builder('example-user-key').set('email', 'test@gmail.com').set('organisation', 'test_org').build()


  def get(self, feature_flag_key: str) -> bool:
    if self.launchdarky_initialized:
      return ldclient.get().variation(feature_flag_key, self.context, False)
      
    return self.default_feature_flag.get(feature_flag_key, False)

# config_ = config.get_config()
config_ = {}
provider = Provider(config_)