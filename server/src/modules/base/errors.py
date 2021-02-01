ERROR_CODES_TO_MESSAGES = {'account_disabled': 'Your account has been disabled by an administrator.'}
AUTHENTICATION_METHOD_CODE_TO_TEXT = {'google': 'Google'}


def get_error_message_from_code(code):
  if code in ERROR_CODES_TO_MESSAGES:
    return ERROR_CODES_TO_MESSAGES[code]

  code_parts = code.split('-')

  if len(code_parts) == 2 and code_parts[0] == 'auth_not_allowed':
    return (f'Your organization does not allow'
            f' signin with {AUTHENTICATION_METHOD_CODE_TO_TEXT.get(code_parts[1], code_parts[1])}.')

  return None
