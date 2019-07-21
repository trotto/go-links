import json
import webapp2

from modules.base.handlers import UserRequiredHandler, get_webapp2_config
from helpers import is_user_admin


class UserHandler(UserRequiredHandler):

  def _write_user_info(self, user):

    self.response.write(json.dumps({
      'email': user.email,
      'admin': is_user_admin(user),
      'role': user.role,
      'notifications': user.notifications
    }))

  def get(self):
    self._write_user_info(self.user)

  def put(self):
    request_data = json.loads(self.request.body)

    self.user.notifications = self.user.notifications or {}
    self.user.notifications.update(request_data.get('notifications', {}))

    self.user.put()

    self._write_user_info(self.user)


app = webapp2.WSGIApplication(
  [
    ('/_/api/users/me', UserHandler)
  ],
  config=get_webapp2_config(),
  debug=False)
