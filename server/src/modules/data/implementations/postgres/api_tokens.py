from __future__ import annotations
import datetime
from typing import Optional

from sqlalchemy_utils.types.encrypted.encrypted_type import EncryptedType

from main import db
from modules.data.abstract import api_tokens
from shared_helpers import config

secret = config.get_config().get('encryption_key') or config.get_config().get('sessions_secret')

class EncryptedCachedType(EncryptedType):
  """
  EncryptedType but with cache.

  SQLAlchemy warns about performance implication without it
  """
  cache_ok = True

class ApiToken(db.Model, api_tokens.ApiToken):

  # Base fields
  id = db.Column(db.Integer, primary_key=True)
  created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  # API token specific
  key = db.Column(EncryptedCachedType(db.String(86), secret), nullable=False) 
  organization = db.Column(db.String(80), nullable=False)
  revoked = db.Column(db.DateTime, nullable=True)


  @staticmethod
  def get_by_id(id: int) -> Optional[ApiToken]:
    return ApiToken.query.get(int(id))

  @staticmethod
  def get_by_key(key: str) -> Optional[ApiToken]:
    return ApiToken.query.filter(ApiToken.key == key).one_or_none()

  @staticmethod
  def get_list() -> list[ApiToken]:
    return ApiToken.query.all()

  def put(self) -> None:
    super().put()

    db.session.add(self)
    db.session.commit()

  def revoke(self) -> None:
    if self.revoked:
      return
    self.revoked = datetime.datetime.utcnow()
    self.put()
