import importlib

from shared_helpers.env import get_database

def get_models(module):
  return importlib.import_module('modules.data.implementations.%s.%s' % (get_database(), module))
