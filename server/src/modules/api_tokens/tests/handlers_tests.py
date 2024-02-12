from typing import Type
import base64
import datetime
import json

from freezegun import freeze_time
import jwt
from mock import patch

from modules.data import get_models
from modules.data.abstract import api_tokens, users
from modules.api_tokens import handlers
from testing import TrottoTestCase


ApiToken: Type[api_tokens.ApiToken] = get_models('api_tokens').ApiToken
User: Type[users.User] = get_models('users').User


BASE_URL = '/_/api/api_tokens'


@patch(
  'shared_helpers.config.get_config',
  return_value={'encryption_key': 'secret', 'admins': ['sam@googs.com']},
)
class TestingApiTokensHandlers(TrottoTestCase):
  blueprints_under_test = [handlers.routes]

  def setUp(self):
    super().setUp()

    self.user = User(
      id=666,
      email='kay@googs.com',
      organization='googs.com',
      domain_type='corporate',
    )
    self.user.put()

    # admin user
    self.admin = User(
      email='sam@googs.com',
      organization='googs.com',
      domain_type='corporate'
    )
    self.admin.put()

  def test_non_admin_gets_403(self, _):
    """Tests all API endpoint with non-admin user"""
    for url, method in (
      (BASE_URL, 'POST'),
      (f'{BASE_URL}/1', 'DELETE'),
      (BASE_URL, 'GET'),
    ):
      with self.subTest():
        response = self.testapp.request(
          url,
          method=method,
          headers={'TROTTO_USER_UNDER_TEST': self.user.email},
          expect_errors=True,
        )
        self.assertEqual(403, response.status_int)

  def test_create_api_token(self, _):
    """Tests successful create"""
    response = self.testapp.post(
      BASE_URL,
      headers={'TROTTO_USER_UNDER_TEST': self.admin.email},
    )

    self.assertEqual(201, response.status_int)
    response = json.loads(response.text)
    self.assertEqual(len(response['key']), 86)
    self.assertEqual(response['organization'], self.admin.organization)
    self.assertEqual(response['revoked'], None)

  
  def test_revoke_api_token(self, _):
    """Tests successful revoke"""
    existed_token = ApiToken(
      key='key',
      organization=self.admin.organization,
    )
    existed_token.put()

    self.assertIsNone(existed_token.revoked)

    mocked_datetime = datetime.datetime(2022, 10, 1, 1, 0, 0)
    with freeze_time(mocked_datetime):
      response = self.testapp.delete(
        f'{BASE_URL}/{existed_token.id}',
        headers={'TROTTO_USER_UNDER_TEST': self.admin.email},
      )

      self.assertEqual(200, response.status_int)
      response = json.loads(response.text)
      self.assertEqual(response['revoked'], str(mocked_datetime))


  def test_revoke_not_found(self, _):
    """Tests revoking unexisting token"""
    response = self.testapp.delete(
      f'{BASE_URL}/999',
      headers={'TROTTO_USER_UNDER_TEST': self.admin.email},
      expect_errors=True,
    )

    self.assertEqual(404, response.status_int)

  def test_get_list(self, _):
    """Testing successfull get for token_list"""
    token_list = [ApiToken(
      key='key',
      organization=self.admin.organization,
    ) for _ in range(10)]
    token_list[4].revoked = datetime.datetime.utcnow()
    for token in token_list:
      token.put()

    response = self.testapp.get(
      BASE_URL,
      headers={'TROTTO_USER_UNDER_TEST': self.admin.email},
    )

    self.assertEqual(200, response.status_int)
    response = json.loads(response.text)
    self.assertEqual(
      {(token.id, token.key, token.revoked and str(token.revoked)) for token in token_list},
      {(res_token['id'], res_token['key'], res_token['revoked']) for res_token in response}
    )
