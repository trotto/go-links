import unittest

import requests
import webtest

from main import init_app_without_routes
from modules.users.helpers import get_or_create_user


class TrottoTestCase(unittest.TestCase):

  def setUp(self):
    self.init_app()

    # always put some data in the database since it seems like in Linux, the datastore emulator
    # can't be reset if there's no data in it (connection refused error)
    get_or_create_user('init@test.trotto.dev', 'test.trotto.dev')

  def tearDown(self):
    # see https://github.com/googleapis/google-cloud-java/issues/1292#issuecomment-250391120
    requests.post('http://localhost:8082/reset')

  def init_app(self):
    app = init_app_without_routes(disable_csrf=True)

    for blueprint in getattr(self, 'blueprints_under_test', []):
      app.register_blueprint(blueprint)

    self.testapp = webtest.TestApp(app)
