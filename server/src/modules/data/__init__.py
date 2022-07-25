import importlib

def get_models(module):
  return importlib.import_module('modules.data.implementations.postgres.%s' % (module))
