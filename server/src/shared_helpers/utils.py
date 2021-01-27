import base64
import os


def generate_secret(number_of_bytes):
  return base64.urlsafe_b64encode(os.urandom(number_of_bytes)).decode('utf-8').strip('=')


def get_from_key_path(a_dict, key_path):
  while key_path:
    if not key_path[0] in a_dict:
      return None

    a_dict = a_dict[key_path[0]]

    key_path = key_path[1:]

  return a_dict
