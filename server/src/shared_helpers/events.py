import time
import uuid

try:
  from commercial.events import EVENT_HANDLERS
except ModuleNotFoundError:
  EVENT_HANDLERS = None


def enqueue_event(event_type, object_type, object_data, timestamp=None):
  if not EVENT_HANDLERS:
    return

  event_timestamp = timestamp or time.time()
  event_id = uuid.uuid4().hex

  object_data['object'] = object_type

  event_object = {'id': event_id,
                  'type': event_type,
                  'created': event_timestamp,
                  'data': {'object': object_data}}

  for handler in EVENT_HANDLERS:
    handler(event_object)
