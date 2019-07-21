def convert_entity_to_dict(entity, allowed_keys, conversion_functions={}):
  return {key: conversion_functions.get(key, lambda val: val)(getattr(entity, key)) for key in allowed_keys}
