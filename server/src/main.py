import os

import jinja2
from flask import Flask, send_from_directory, redirect, request
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf

from shared_helpers.env import get_database
from shared_helpers.configs import get_secrets

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'static')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def init_app_without_routes(disable_csrf=False):
  app = Flask(__name__)

  app.secret_key = get_secrets()['sessions_secret']

  if get_database() == 'postgres':
    app.config['SQLALCHEMY_DATABASE_URI'] = get_secrets()['postgres']['url']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    global db
    global migrate
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

  if os.getenv('ENVIRONMENT') == 'test_env':
    from modules.base.authentication import login_test_user

    app.before_request(login_test_user)

  login_manager = LoginManager()
  login_manager.init_app(app)

  if not disable_csrf:
    csrf_protect = CSRFProtect()
    csrf_protect.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    return get_user_by_id(user_id)

  return app


app = init_app_without_routes()


from modules.base.handlers import routes as base_routes
from modules.links.handlers import routes as link_routes
from modules.routing.handlers import routes as follow_routes
from modules.users.handlers import routes as user_routes
from modules.users.helpers import get_user_by_id


app.register_blueprint(base_routes)
app.register_blueprint(link_routes)
app.register_blueprint(user_routes)
app.register_blueprint(follow_routes)  # must be registered last since it matches any URL


@app.route('/')
def home():
  if not current_user.is_authenticated:
    return redirect('https://www.trot.to'
                    if request.host == 'trot.to'
                    else '/_/auth/login')

  template = JINJA_ENVIRONMENT.get_template('index.html')

  return template.render({'csrf_token': generate_csrf()})

@app.route('/_styles/<path:path>')
@app.route('/_scripts/<path:path>')
@app.route('/_images/<path:path>')
def static_files(path):
  return send_from_directory('static/%s' % (request.path.split('/')[1]), path)
