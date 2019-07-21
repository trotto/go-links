import datetime
import os
import urllib

from google.appengine.ext import deferred

import jinja2
from validate_email import validate_email

import models
from modules.organizations.utils import get_organization_id_for_email
from shared_helpers import configs
from shared_helpers import email as email_helper
from shared_helpers.encoding import convert_entity_to_dict
from shared_helpers.events import enqueue_event
from shared_helpers import utils


JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../../static/templates')),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)


class LoginEmailException(Exception):
  pass


class LoginLinkValidationError(Exception):
  pass


def _extract_domain_type(email):
  return 'generic' if '@' in get_organization_id_for_email(email) else 'corporate'


def get_or_create_user(email, user_org):
  email = email.lower()

  user = models.User.query(
    models.User.email == email
  ).get()

  # TODO: Remove this when all users are backfilled
  if user and (not user.domain_type
               or not user.organization):
    user.domain_type = _extract_domain_type(email)

    if not user.organization:
      user.organization = user.extract_organization()

    user.put()

  if not user:
    user = models.User(email=email,
                       domain_type=_extract_domain_type(email))
    user.organization = user.extract_organization()
    user.put()

    enqueue_event('user.created',
                  'user',
                  convert_entity_to_dict(user, ['oid', 'email', 'organization']))

  return user


def send_login_email(request_source_url, email):
  if not validate_email(email):
    raise LoginEmailException('Please provide a valid email address')

  email_login_link_object = models.EmailLoginLink(email=email,
                                                  secret=utils.generate_secret(32))
  email_login_link_object.put()

  html_template = JINJA_ENVIRONMENT.get_template('auth/login_link_email.html')
  txt_template = JINJA_ENVIRONMENT.get_template('auth/login_link_email.txt')

  if '/play_queued_request' in request_source_url:
    emailed_url = request_source_url
  else:
    scheme, remainder = request_source_url.split('://')
    emailed_url = '%s://%s/_/auth/email_callback' % (scheme, remainder.split('/')[0])

  login_url = '%s?%s' % (emailed_url,
                         urllib.urlencode({'e': email, 's': email_login_link_object.secret}))

  html = html_template.render({'login_url': login_url})
  text = txt_template.render({'login_url': login_url})

  email_data = {'recipient_email': email,
                'subject': 'Log in to Trotto',
                'plaintext': text,
                'html': html}

  deferred.defer(email_helper.send_email,
                 email_data)


def validate_login_link(email, secret):
  LINK_DURATION_IN_MINS = 15

  if not email or not secret:
    raise LoginLinkValidationError()

  match = models.EmailLoginLink.query(models.EmailLoginLink.email == email,
                                      models.EmailLoginLink.secret == secret).get()

  if not match:
    raise LoginLinkValidationError('Invalid login link')

  if not match or match.used:
    raise LoginLinkValidationError('This login link has already been used. Login links may only be used once.')

  if match.created < (datetime.datetime.utcnow() - datetime.timedelta(minutes=LINK_DURATION_IN_MINS)):
    raise LoginLinkValidationError(
      'This login link has expired. Links are valid for %s minutes' % (LINK_DURATION_IN_MINS))

  match.used = True
  match.put()


def is_user_admin(user):
  org_config = configs.get_organization_config(user.organization)

  return user.email in org_config.get('admins', []) if org_config else False
