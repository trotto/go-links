import importlib
import os
import subprocess
import unittest

import webtest

import main


class TrottoTestCase(unittest.TestCase):

  def setUp(self):
    main.db.close_all_sessions()
    main.db.engine.dispose()

    subprocess.run(['bash', os.getenv('CLEAR_POSTGRES_DB_SCRIPT')], stdout=subprocess.DEVNULL)

    self.init_app()

  def init_app(self):
    importlib.reload(main)

    app = main.init_app_without_routes(disable_csrf=True)

    for blueprint in getattr(self, 'blueprints_under_test', []):
      app.register_blueprint(blueprint)

    self.testapp = webtest.TestApp(app)
