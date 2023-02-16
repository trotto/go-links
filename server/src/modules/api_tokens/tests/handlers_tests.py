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
# from ....testing import TrottoTestCase


ApiToken: Type[api_tokens.ApiToken] = get_models('api_tokens').ApiToken
User: Type[users.User] = get_models('users').User


BASE_URL = '/_/api/api_tokens'


@patch('shared_helpers.config.get_config', return_value={'encryption_key': 'secret',
                                                         'admins': ['sam@googs.com']})
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
    response = self.testapp.delete(
      f'{BASE_URL}/999',
      headers={'TROTTO_USER_UNDER_TEST': self.admin.email},
      expect_errors=True,
    )

    self.assertEqual(404, response.status_int)

  def test_get_list(self, _):
    response = self.testapp.get(
      BASE_URL,
      headers={'TROTTO_USER_UNDER_TEST': self.admin.email},
    )

    print(response.text)

    self.assertEqueal(True, False)


  # def test_get_transfer_link__authorized_admin(self, _):
  #   next_year = datetime.datetime.utcnow().year + 1
  #   with freeze_time(datetime.datetime(next_year, 10, 1, 1, 0, 0)):
#       response = self.testapp.post('/_/api/links/7/transfer_link',
#                                    headers={'TROTTO_USER_UNDER_TEST': 'sam@googs.com'})

#     self.assertEqual(201, response.status_int)

#     expected_jwt = jwt.encode({'exp': datetime.datetime(next_year, 10, 2, 1, 0, 0),
#                                'sub': 'link:7',
#                                'tp': 'transfer',
#                                'o': self.test_user.id,
#                                'by': User.get_by_email_and_org('sam@googs.com', 'googs.com').id},
#                               'the_secret',
#                               algorithm='HS256')

#     expected_url = f"http://localhost/_transfer/{self._get_transfer_token(expected_jwt)}"

#     self.assertEqual({'url': expected_url},
#                      response.json)

#   def test_get_transfer_link__user_only_has_read_access(self, _):
#     response = self.testapp.post('/_/api/links/7/transfer_link',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'jay@googs.com'},
#                                  expect_errors=True)
#     self.assertEqual(403, response.status_int)

#   def test_get_transfer_link__no_such_link(self, _):
#     response = self.testapp.post('/_/api/links/10/transfer_link',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'},
#                                  expect_errors=True)
#     self.assertEqual(403, response.status_int)

#   def test_use_transfer_link__jwt_expired(self, _):
#     minute_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
#     self.token_payload.update({'exp': minute_ago})

#     transfer_token = self._get_transfer_token()

#     response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
#                                  expect_errors=True)
#     self.assertEqual(403, response.status_int)
#     self.assertEqual({'error_type': 'error_bar',
#                       'error': 'Your transfer link has expired'},
#                      response.json)

#   def test_use_transfer_link__jwt_invalid_signature(self, _):
#     invalid_jwt = jwt.encode(self.token_payload, 'no_secret', algorithm='HS256')
#     transfer_token = self._get_transfer_token(invalid_jwt)

#     response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
#                                  expect_errors=True)
#     self.assertEqual(403, response.status_int)

#   def test_use_transfer_link__inapplicable_subject(self, _):
#     self.token_payload.update({'sub': 'link_something:7'})

#     transfer_token = self._get_transfer_token()

#     response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
#                                  expect_errors=True)
#     self.assertEqual(403, response.status_int)

#   def test_use_transfer_link__jwt_missing_claims(self, _):
#     del self.token_payload['tp']

#     transfer_token = self._get_transfer_token()

#     response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
#                                  expect_errors=True)
#     self.assertEqual(403, response.status_int)

#   def test_use_transfer_link__invalid_permission(self, _):
#     self.token_payload.update({'tp': 'read'})

#     transfer_token = self._get_transfer_token()

#     response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
#                                  expect_errors=True)
#     self.assertEqual(403, response.status_int)

#   def test_use_transfer_link__no_such_link(self, _):
#     self.token_payload.update({'sub': 'link:20'})

#     transfer_token = self._get_transfer_token()

#     response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
#                                  expect_errors=True)
#     self.assertEqual(403, response.status_int)

#   def test_use_transfer_link__owner_does_not_match(self, _):
#     User(id=20,
#          email='al@googs.com',
#          organization='googs.com',
#          domain_type='corporate'
#          ).put()

#     self.token_payload.update({'o': 20})

#     transfer_token = self._get_transfer_token()

#     response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
#                                  expect_errors=True)
#     self.assertEqual(403, response.status_int)
#     self.assertEqual({'error_type': 'error_bar',
#                       'error': 'The owner of go/there has changed since your transfer link was created'},
#                      response.json)

#   def test_use_transfer_link__token_from_user_without_access(self, _):
#     User(id=20,
#          email='al@googs.com',
#          organization='googs.com',
#          domain_type='corporate'
#          ).put()

#     self.token_payload.update({'by': 20})

#     transfer_token = self._get_transfer_token()

#     response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'},
#                                  expect_errors=True)
#     self.assertEqual(403, response.status_int)
#     self.assertEqual({'error_type': 'error_bar',
#                       'error': 'The user who created your transfer link no longer has edit rights for go/there'},
#                      response.json)

#   def test_use_transfer_link__accepting_user_in_wrong_org(self, _):
#     transfer_token = self._get_transfer_token()

#     response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'joe@other.com'},
#                                  expect_errors=True)
#     self.assertEqual(403, response.status_int)

#     link = ShortLink.get_by_id(7)

#     self.assertEqual('kay@googs.com', link.owner)

#   def test_use_transfer_link__success(self, _):
#     transfer_token = self._get_transfer_token()

#     response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'})
#     self.assertEqual(201, response.status_int)

#     updated_link = ShortLink.get_by_id(7)

#     self.assertEqual('joe@googs.com', updated_link.owner)

#   def test_use_transfer_link__success__generated_by_admin(self, _):
#     self.token_payload.update({'by': User.get_by_email_and_org('sam@googs.com', 'googs.com').id})

#     transfer_token = self._get_transfer_token()

#     response = self.testapp.post(f'/_/api/transfer_link/{transfer_token}',
#                                  headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'})
#     self.assertEqual(201, response.status_int)

#     updated_link = ShortLink.get_by_id(7)

#     self.assertEqual('joe@googs.com', updated_link.owner)

#   def test_redirect_transfer_url__signed_in(self, _):
#     response = self.testapp.get('/_transfer/my_token',
#                                 headers={'TROTTO_USER_UNDER_TEST': 'joe@googs.com'})

#     self.assertEqual(302, response.status_int)
#     self.assertEqual('http://localhost/?transfer=my_token', response.location)

#   def test_redirect_transfer_url__not_signed_in(self, _):
#     response = self.testapp.get('/_transfer/my_token')

#     self.assertEqual(302, response.status_int)
#     self.assertEqual('http://localhost/_/auth/login?redirect_to=%2F_transfer%2Fmy_token%3F',
#                      response.location)


# class TestKeywordPunctuationSensitivityConfig(TrottoTestCase):

#   blueprints_under_test = [handlers.routes]

#   TEST_KEYWORD = 'meeting-notes'
#   TEST_DESTINATION = 'https://docs.google.com/document/d/2Bd5X-6WFpRbafPgXax98GZenmCTZkTrNxotNvb8k2vI/edit'

#   def _create_link(self, keyword):
#     response = self.testapp.post_json('/_/api/links',
#                                       {'shortpath': keyword,
#                                        'destination': self.TEST_DESTINATION},
#                                       headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

#     return response.json

#   @patch('shared_helpers.config.get_organization_config',
#          return_value={})
#   def test_keyword_punctuation_sensitivity__not_specified(self, _):
#     response = self._create_link(self.TEST_KEYWORD)

#     self.assertEqual(self.TEST_KEYWORD, response.get('shortpath'))

#     keyword_without_dashes = self.TEST_KEYWORD.replace('-', '')

#     response = self._create_link(keyword_without_dashes)

#     self.assertEqual(keyword_without_dashes, response.get('shortpath'))

#   @patch('shared_helpers.config.get_organization_config',
#          return_value={'keywords': {'punctuation_sensitive': False}})
#   def test_keyword_punctuation_sensitivity__insensitive(self, _):
#     response = self._create_link(self.TEST_KEYWORD)

#     self.assertEqual(self.TEST_KEYWORD, response.get('shortpath'))

#     keyword_without_dashes = self.TEST_KEYWORD.replace('-', '')

#     response = self._create_link(keyword_without_dashes)

#     self.assertIn(self.TEST_KEYWORD, response.get('error'))

#     response = self.testapp.get('/_/api/links',
#                                 headers={'TROTTO_USER_UNDER_TEST': 'kay@googs.com'})

#     self.assertEqual(1, len(response.json))

#     self.assertEqual(self.TEST_KEYWORD, response.json[0]['shortpath'])
