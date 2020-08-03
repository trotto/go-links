import json

from modules.data import get_models
from modules.users import handlers
from testing import TrottoTestCase


User = get_models('users').User


class TestUserHandlers(TrottoTestCase):

  blueprints_under_test = [handlers.routes]

  def test_user_info_endpoint(self):
    User(id=777,
         email='kay@googs.com',
         domain_type='corporate',
         notifications={'some_announcement': 'dismissed'}).put()

    User(id=8675,
         email='ray@googs.com',
         domain_type='corporate').put()

    response = self.testapp.get('/_/api/users/me',
                                headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

    self.assertEqual(json.loads(response.text),
                     {'email': 'kay@googs.com',
                      'role': None,
                      'admin': False,
                      'notifications': {'some_announcement': 'dismissed'}})

    response = self.testapp.get('/_/api/users/me',
                                headers={'TROTTO_USER_UNDER_TEST': 'ray@googs.com'})

    self.assertEqual(json.loads(response.text),
                     {'email': 'ray@googs.com',
                      'role': None,
                      'admin': False,
                      'notifications': {}})
