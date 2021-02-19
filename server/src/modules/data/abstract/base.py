# Modeled off of
# https://github.com/GoogleCloudPlatform/datastore-ndb-python/blob/cf4cab3f1f69cd04e1a9229871be466b53729f3f/ndb/model.py.
#
# Copyright 2008 The ndb Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime

try:
  from commercial.data.utils import allocate_id
except ModuleNotFoundError:
  allocate_id = None


class BaseModel(object):
  id = int
  created = datetime
  modified = datetime
  modified_override = None

  def __init__(self, **kwargs):
    self._set_attributes(kwargs)

  def _set_attributes(self, kwds):
    cls = self.__class__

    for name in self._properties:
      value = kwds.get(name, None)

      expected_type = getattr(cls, name)  # Raises AttributeError for unknown properties.
      if value and not isinstance(value, expected_type):
        raise TypeError('"%s" property must be of type %s. Instead is %s.' % (name, expected_type, type(value)))
      setattr(self, name, value)

  def get_id(self):
    return self.id

  def put(self):
    self.modified = self.modified_override or datetime.utcnow()
    if not self.id:
      self.created = datetime.utcnow()

    if not self.id and allocate_id:
      self.id = allocate_id(self)
