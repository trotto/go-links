from typing import Type

from modules.data import get_models
from modules.data.abstract.api_tokens import ApiToken as ApiTokenABC

ApiToken: Type[ApiTokenABC] = get_models('api_tokens').ApiToken

def get_token_by_key(key: str) -> ApiTokenABC:
  return ApiToken.get_by_key(key)
