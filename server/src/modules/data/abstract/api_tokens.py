from __future__ import annotations
from datetime import datetime
from typing import Optional

from modules.data.abstract.base import BaseModel


class ApiToken(BaseModel):
  key = str
  organization = str
  revoked = datetime
  

  # TODO: Eliminate the need for this duplication with a better base class.
  _properties = ['id', 'created', 'modified', 'organization', 'revoked', 'key']

  def __eq__(self, other: ApiToken) -> bool:
    # simple comparison for unit tests
    return self.id == other.id if self.id else self.key == other.key

  def revoke() -> None:
    raise NotImplementedError

  @staticmethod
  def get_by_id(id: int) -> Optional[ApiToken]:
    raise NotImplementedError

  @staticmethod
  def get_by_key(id: str) -> Optional[ApiToken]:
    raise NotImplementedError

  @staticmethod
  def get_list() -> list[ApiToken]:
    raise NotImplementedError
