from citrination_client.base import BaseClient
from citrination_client.errors import CitrinationClientError

def test_none_api_key():
  try:
    client = BaseClient(None)
    assert False
  except CitrinationClientError:
    assert True

def test_zero_length_api_key():
  try:
    client = BaseClient("")
    assert False
  except CitrinationClientError:
    assert True