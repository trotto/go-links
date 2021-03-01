import json
import logging
import os
import traceback

import jinja2
from flask import Flask, send_from_directory, redirect, request, jsonify
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from flask_migrate import Migrate, upgrade as upgrade_db
from flask_wtf.csrf import generate_csrf
import sentry_sdk
from werkzeug.routing import BaseConverter

from shared_helpers import config


sentry_config = config.get_config_by_key_path(['monitoring', 'sentry'])
if sentry_config:
  from sentry_sdk.integrations.flask import FlaskIntegration

  sentry_sdk.init(dsn=sentry_config['dsn'],
                  integrations=[FlaskIntegration()],
                  traces_sample_rate=sentry_config.get('traces_sample_rate', 0.1))


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'static')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def init_app_without_routes(disable_csrf=False):
  app = Flask(__name__)

  app.secret_key = config.get_config()['sessions_secret']

  app.config['SQLALCHEMY_DATABASE_URI'] = config.get_config()['postgres']['url']

  if config.get_config()['postgres'].get('commercial_url'):
    app.config['SQLALCHEMY_BINDS'] = {'commercial': config.get_config()['postgres']['commercial_url']}

  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  global db
  class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True
  db = SQLAlchemy(app)

  from modules.base import authentication

  if os.getenv('ENVIRONMENT') == 'test_env':
    app.before_request(authentication.login_test_user)

  @app.errorhandler(403)
  def handle_403(error):
    return jsonify({'error_type': 'error_bar',
                    'error': error.description or ''
                    }), 403

  login_manager = LoginManager()
  login_manager.init_app(app)

  global csrf_protect

  if not disable_csrf:
    app.before_request(authentication.check_csrf)

  @login_manager.user_loader
  def load_user(user_id):
    from modules.users.helpers import get_user_by_id

    sentry_sdk.set_user({'id': user_id})

    return get_user_by_id(user_id)

  app.before_request(authentication.validate_user_authentication)


  @app.route('/_/health_check')
  def health_check():
    return 'OK'

  return app


app = init_app_without_routes()


with app.app_context():
  try:
    global migrate

    migrate = Migrate(app, db)

    if os.getenv('POSTGRES_UPGRADE_ON_START', '').lower() == 'true':
      upgrade_db(directory=os.path.join(os.path.dirname(__file__), 'migrations'))
  except:
    logging.warning("Exception from Flask-Migrate/Alembic. This may be expected if you've deployed a new version of the"
                    " app and an older version hasn't finished shutting down, or you've rolled back versions. %s",
                    traceback.format_exc())


class RegexConverter(BaseConverter):

  def __init__(self, map, *items):
    super(RegexConverter, self).__init__(map)
    self.regex = items[0] if items else ''


app.url_map.converters['regex'] = RegexConverter


def add_routes():
  from modules.base.handlers import routes as base_routes
  from modules.links.handlers import routes as link_routes
  from modules.routing.handlers import routes as follow_routes
  from modules.users.handlers import routes as user_routes
  try:
    from commercial.blueprints import COMMERCIAL_BLUEPRINTS
  except ModuleNotFoundError:
    COMMERCIAL_BLUEPRINTS = []

  app.register_blueprint(base_routes)
  app.register_blueprint(link_routes)
  app.register_blueprint(user_routes)
  for blueprint in COMMERCIAL_BLUEPRINTS:
    app.register_blueprint(blueprint)
  app.register_blueprint(follow_routes)  # must be registered last since it matches any URL

add_routes()

@app.route('/')
def home():
  if not current_user.is_authenticated:
    return redirect('https://www.trot.to'
                    if request.host == 'trot.to'
                    else '/_/auth/login')

  template = JINJA_ENVIRONMENT.get_template('index.html')

  namespaces = config.get_organization_config(current_user.organization).get('namespaces', [])

  return template.render({'csrf_token': generate_csrf(),
                          'default_namespace': config.get_default_namespace(current_user.organization),
                          'namespaces': json.dumps(namespaces)})


@app.route('/_scripts/config.js')
def layout_config():
  layout_json = json.dumps(config.get_config().get('layout', {}))
  return f"window._trotto = window._trotto || {{}}; window._trotto.layout = {layout_json};"


@app.route('/_styles/<path:path>')
@app.route('/_scripts/<path:path>')
@app.route('/_images/<path:path>')
def static_files(path):
  return send_from_directory('static/%s' % (request.path.split('/')[1]), path)
