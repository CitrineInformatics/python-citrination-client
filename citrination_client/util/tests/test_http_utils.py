from citrination_client.util.http import get_success_json
from requests.models import Response
from citrination_client.errors import CitrinationClientError

import requests


def test_raises_client_error_if_not_200():
  r = Response()
  r.status_code = requests.codes.bad
  try:
    get_success_json(r)
    assert False
  except CitrinationClientError:
    assert True