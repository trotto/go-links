import requests

import configs


def send_email(data):
  NOREPLY_EMAIL = 'no-reply@trot.to'

  mailgun_request_data = {"from": "%s <%s>" % (data.get('sender_name', 'Team Trotto'),
                                               data.get('reply_to', NOREPLY_EMAIL)),
                          "to": data['recipient_email'],
                          "subject": data['subject'],
                          "text": data['plaintext'],
                          "html": data['html']}

  if data.get('html') is not None:
    mailgun_request_data['html'] = data['html']

  response = requests.post("https://api.mailgun.net/v3/mg.trot.to/messages",
                           auth = ("api", configs.get_config()['mailgun']['general_use_api_key']),
                           data = mailgun_request_data)

  response.raise_for_status()
