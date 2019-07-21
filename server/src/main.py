import os

from google.appengine.api.modules import modules

import jinja2
import webapp2

from modules.base.handlers import BaseHandler, get_webapp2_config

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'static')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(BaseHandler):

    def check_authorization(self):
        pass

    def get(self):
        if not self.user:
          self.redirect('https://www.trot.to'
                        if self.request.host == 'trot.to'
                        else '/_/auth/login')

        template = JINJA_ENVIRONMENT.get_template('index.html')

        self.response.write(template.render(
            {'app_version_id': modules.get_current_version_name(),
             'alreadyAcceptedTerms': self.session.get('already_accepted_terms', False),
             'csrf_token': self.session.get('csrf_token', '')}
        ))

app = webapp2.WSGIApplication(
    [('/', MainHandler)],
    config=get_webapp2_config(),
    debug=False
)
