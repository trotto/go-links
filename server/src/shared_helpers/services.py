import datetime
import logging
from urllib.parse import urljoin

import jwt
import requests

from shared_helpers.config import get_config_by_key_path, get_service_config


INTERNAL_TOKEN_HEADER = 'X-Token'
SIGNING_ALGORITHM = 'HS256'


class InvalidInternalToken(Exception):
  pass


TOKEN_DURATION_IN_SECONDS = 30


def _create_internal_token(service_id, payload):
  payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=TOKEN_DURATION_IN_SECONDS)

  return jwt.encode(payload,
                    get_service_config(service_id)['signing_secret'],
                    algorithm=SIGNING_ALGORITHM)


def get(service_id, path):
  full_url = urljoin(get_service_config(service_id)['base_url'] + '/',
                     path.strip('/'))

  payload = {'url': full_url}

  response = requests.get(full_url,
                          headers={INTERNAL_TOKEN_HEADER: _create_internal_token(service_id, payload)})

  response.raise_for_status()

  return response.json()


def validate_internal_request(request):
  internal_token = request.headers.get(INTERNAL_TOKEN_HEADER)

  if not internal_token:
    raise InvalidInternalToken('no token')

  try:
    decoded_data = jwt.decode(internal_token,
                              get_config_by_key_path(['signing_secret']),
                              algorithms=[SIGNING_ALGORITHM])

    if 'exp' not in decoded_data:
      logging.warning('Someone attempted to use an invalid internal token: %s', internal_token)

      raise InvalidInternalToken('missing exp')
  except jwt.exceptions.InvalidSignatureError:
    logging.warning('Someone attempted to use an invalid internal token: %s', internal_token)

    raise InvalidInternalToken('invalid signature')
  except jwt.exceptions.ExpiredSignatureError:
    logging.warning('Someone attempted to use an expired internal token: %s', internal_token)

    raise InvalidInternalToken('expired')

  if request.url != decoded_data['url']:
    logging.warning('Someone attempted to use an internal token with the'
                    ' wrong URL. Token URL: %s. Request URL: %s. Token: %s',
                    decoded_data['url'], request.url, internal_token)

    raise InvalidInternalToken('mismatched URL')

  return True
