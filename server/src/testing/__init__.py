import base64
import importlib
import multiprocessing
import os
import subprocess
import unittest

import requests
import webtest
import yaml

import main

multiprocessing.set_start_method('fork')

LIVE_APP_HOST = 'http://localhost:5010'

class TrottoTestCase(unittest.TestCase):

  def setUp(self):
    main.db.close_all_sessions()
    main.db.engine.dispose()

    subprocess.run(['bash', os.getenv('CLEAR_POSTGRES_DB_SCRIPT')], stdout=subprocess.DEVNULL)

    self.init_app()

    if getattr(self, 'start_live_app', False):
      self.prior_trotto_config = os.getenv('TROTTO_CONFIG')

      os.environ['TROTTO_CONFIG'] = base64.b64encode(
          yaml.dump(self.live_app_config, encoding='utf-8')).decode(('utf-8'))

      # TODO: Surface errors from the server process if a test fails.
      self.server_process = multiprocessing.Process(target=self.realapp.run, kwargs={'host': 'localhost',
                                                                                     'port': 5010})
      self.server_process.start()

      while True:
        try:
          if 200 == requests.get(f'{LIVE_APP_HOST}/_/health_check').status_code:
            break
        except requests.exceptions.ConnectionError:
          pass

  def tearDown(self):
    if getattr(self, 'start_live_app', False):
      if self.prior_trotto_config:
        os.environ['TROTTO_CONFIG'] = self.prior_trotto_config
      else:
        del os.environ['TROTTO_CONFIG']

      self.server_process.terminate()
      self.server_process.join()

  def init_app(self):
    importlib.reload(main)

    self.realapp = main.init_app_without_routes(disable_csrf=True)

    for blueprint in getattr(self, 'blueprints_under_test', []):
      self.realapp.register_blueprint(blueprint)

    self.testapp = webtest.TestApp(self.realapp)

