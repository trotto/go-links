from flask_login import current_user

import time
import uuid

try:
  from commercial.events import EVENT_HANDLERS
except ModuleNotFoundError:
  EVENT_HANDLERS = None


def enqueue_event(org_id, event_type, object_type, object_data, timestamp=None, user=None):
  if not EVENT_HANDLERS:
    return

  event_timestamp = timestamp or time.time()
  event_id = uuid.uuid4().hex

  object_data['object'] = object_type

  event_object = {'id': event_id,
                  'type': event_type,
                  'created': event_timestamp,
                  'organization': org_id,
                  'data': {'object': object_data}}

  user_for_event = user or current_user

  if user_for_event and hasattr(user_for_event, 'email'):
    event_object['data']['user'] = {'object': 'user',
                                    'email': user_for_event.email}

  for handler in EVENT_HANDLERS:
    handler(event_object)
