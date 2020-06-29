import base64
import json
import logging
import pickle

from oauth2client.client import FlowExchangeError
import webapp2

import helpers
import models
from modules.base import authentication
from modules.base.handlers import UserRequiredHandler, NoLoginRequiredHandler, get_webapp2_config
from modules.organizations.utils import get_organization_id_for_email
from modules.users import helpers as user_helpers
from shared_helpers.encoding import convert_entity_to_dict
from shared_helpers.events import enqueue_event


class LinksHandler(UserRequiredHandler):

  ALLOWED_KEYS = ['oid', 'created', 'owner', 'shortpath', 'destination_url', 'visits_count']

  def get_field_conversion_fns(self):
    return {
      'visits_count': (lambda count: count or 0),
      'created': str
    }

  def check_authorization(self):
    UserRequiredHandler.check_authorization(self)

    self.existing_link = None

    if self.request.route_kwargs and self.request.route_kwargs.get('link_id'):
      try:
        self.existing_link = models.ShortLink.get_by_id(int(self.request.route_kwargs.get('link_id')))
      except Exception as e:
        logging.warning(str(e))

      if (self.existing_link
          and self.existing_link.owner != self.user_email
          and not (self.user.organization == self.existing_link.organization
                   and user_helpers.is_user_admin(self.user))):
        self.abort(403)

  def _write_link_to_response(self, link):
    self.response.write(json.dumps(
      convert_entity_to_dict(link, self.ALLOWED_KEYS, self.get_field_conversion_fns())
    ))

  def get(self):
    links = [convert_entity_to_dict(entity, self.ALLOWED_KEYS, self.get_field_conversion_fns())
             for entity in helpers.get_all_shortlinks_for_org(self.user_org)]

    for link in links:
      link['mine'] = link['owner'] == self.user_email

    self.response.write(json.dumps(links))

  def post(self):
    object_data = json.loads(self.request.body)

    try:
      new_link = helpers.create_short_link(self.user_org,
                                           self.user_email,
                                           object_data['shortpath'],
                                           object_data['destination'])
    except helpers.LinkCreationException as e:
      self.response.write(json.dumps({
        'error': str(e)
      }))
      return

    self.response.write(
      json.dumps(convert_entity_to_dict(new_link, self.ALLOWED_KEYS, self.get_field_conversion_fns()))
    )

  def put(self, **kwargs):
    if not self.existing_link:
      self.abort(400)

    object_data = json.loads(self.request.body)

    self.existing_link.destination_url = object_data['destination']

    try:
      self._write_link_to_response(
        helpers.update_short_link(self.existing_link)
      )
    except helpers.LinkCreationException as e:
      self.response.write(json.dumps({
        'error': str(e),
        'error_type': 'error_bar'
      }))
      return

  def delete(self, **kwargs):
    if not self.existing_link:
      self.abort(400)

    logging.info('Deleting link: %s' % (convert_entity_to_dict(self.existing_link, self.ALLOWED_KEYS)))

    self.existing_link.key.delete()

    enqueue_event('link.deleted',
                  'link',
                  convert_entity_to_dict(self.existing_link, self.ALLOWED_KEYS, self.get_field_conversion_fns()))

    self.response.write('{}')


class PlayQueuedCreationHandler(NoLoginRequiredHandler):

  def get(self):
    if self.request.get('r'):  # outgoing request
      self.session['request_data_to_replay'] = str(self.request.get('r'))

      self.render_login_selector_page(self.request.path_url)
      return

    try:
      original_request_data = json.loads(base64.urlsafe_b64decode(self.session['request_data_to_replay']))
    except (KeyError, ValueError):
      self.redirect('/')
      return

    if self.request.get('code'):
      flow = pickle.loads(self.session['pickled_oauth_flow'])

      try:
        credentials = flow.step2_exchange(self.request.get('code'))
      except (FlowExchangeError, ValueError):
        # user declined to auth; move on
        self.redirect(original_request_data['origin'])
        return

      self.session['credentials'] = pickle.dumps(credentials)

      self.session['user_email'] = authentication.get_user_email(credentials)
      self.user_email = self.session['user_email']
      self.user_org = get_organization_id_for_email(self.user_email)
    else:
      # assume this was a login via email, which would have been processed in the base handler
      pass

    object_data = json.loads(original_request_data['body'])

    new_link = None

    try:
      new_link = helpers.create_short_link(self.user_org,
                                           self.user_email,
                                           object_data['shortpath'],
                                           object_data['destination'])
      response_data = {
        'shortpath': new_link.shortpath,
        'destination': new_link.destination_url
      }
    except helpers.LinkCreationException as e:
      response_data = {
        'error': str(e)
      }

    self.redirect(str(original_request_data['origin'] + '?r=' + base64.urlsafe_b64encode(json.dumps(response_data))))


app = webapp2.WSGIApplication(
  [
    ('/_/api/links', LinksHandler),
    webapp2.Route('/_/api/links/<link_id:\d+>', LinksHandler),
    ('/_/api/links/play_queued_request', PlayQueuedCreationHandler)
  ],
  config=get_webapp2_config(),
  debug=False)
