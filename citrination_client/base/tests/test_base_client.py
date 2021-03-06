from citrination_client.base import BaseClient
from citrination_client.base.errors import CitrinationClientError
from citrination_client import __version__

def test_none_api_key():
  """
  Ensures that an error is thrown if a client is instantiated
  without an API key
  """
  try:
    client = BaseClient(None, "mycitrinationsite")
    assert False
  except CitrinationClientError:
    assert True

def test_zero_length_api_key():
  """
  Tests that a zero length API key will cause the client to throw
  an error on instantiation
  """
  try:
    client = BaseClient("", "mycitrinationsite")
    assert False
  except CitrinationClientError:
    assert True

def test_version():
  """
  Tests that the version is extracted
  """
  ver = __version__
  print("Version:" + ver)
  assert ver[0].isdigit()

