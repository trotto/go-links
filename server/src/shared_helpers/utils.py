import base64
import os


def generate_secret(number_of_bytes):
  return base64.urlsafe_b64encode(os.urandom(number_of_bytes)).decode('utf-8').strip('=')
