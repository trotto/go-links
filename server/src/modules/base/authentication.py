import httplib2

from apiclient.discovery import build


def get_user_email(oauth_credentials):
  http = httplib2.Http()
  http = oauth_credentials.authorize(http)

  user_info = build('oauth2', 'v2').tokeninfo().execute(http)

  if not user_info['verified_email']:
    return None

  return user_info['email'].lower()
