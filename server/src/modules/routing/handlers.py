import time
import urllib

import webapp2

from modules.base import authentication
from modules.base.handlers import NoLoginRequiredHandler, get_webapp2_config
from modules.links.helpers import get_shortlink
from shared_helpers.events import enqueue_event


class RedirectHandler(NoLoginRequiredHandler):

  def queue_event(self, followed_at, shortlink_id, destination, accessed_via, email=None):
    enqueue_event('link_follow.created',
                  'link_follow',
                  {'link_id': shortlink_id,
                   'user_email': email or self.user_email,
                   'access_method': accessed_via,
                   'destination': destination},
                  followed_at)

  def get(self):
    requested_at = time.time()

    provided_shortpath = urllib.unquote(self.request.path.strip('/'))
    shortpath_parts = provided_shortpath.split('/', 1)
    shortpath = '/'.join([shortpath_parts[0].lower()] + shortpath_parts[1:])

    if not self.user_email:
      if shortpath == 'welcome' or shortpath == 'trotto-welcome':
        WALKTHROUGH_SAMPLE_DOC = 'https://docs.google.com/document/d/1B-M6yw-mqEl9U2cc2VKIwvOF_jCSrGByga9k7z4sxBQ/edit'
        self.redirect(WALKTHROUGH_SAMPLE_DOC)
        return

      if shortpath == 'trotto-init':
        WALKTHROUGH_POST_INSTALL = 'https://www.trot.to/getting-started?installed=true#steps'
        self.redirect(WALKTHROUGH_POST_INSTALL)
        return

      if self.request.get('s') == 'crx' and self.request.get('sc'):
        # see: go/484356182846856
        self.force_to_original_url()
        return

      self.redirect('/_/auth/login?%s' % urllib.urlencode({'redirect_to': self.request.path_qs}))
      return

    matching_shortlink, destination = get_shortlink(self.user_org, shortpath)

    if matching_shortlink:
      self.queue_event(requested_at,
                       matching_shortlink.key.id(),
                       destination,
                       self.request.get('s') or 'other')
      self.redirect(str(destination))
    elif self.request.get('s') == 'crx' and self.request.get('sc'):
      self.force_to_original_url()
    else:
      self.redirect(
        '%s/?%s'
        % ('http://localhost:5007' if self.request.host.startswith('localhost') else '',
           urllib.urlencode({'sp': shortpath}))
      )


app = webapp2.WSGIApplication(
  [
    ('.*', RedirectHandler),
  ],
  config=get_webapp2_config(),
  debug=False)
