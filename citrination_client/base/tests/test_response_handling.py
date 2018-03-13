from citrination_client.base.response_handling import raise_on_response
from citrination_client.base.errors import *
from requests.models import Response
import requests

response_exceptions = [{
        "code": requests.codes.server_error,
        "exception_class": CitrinationServerErrorException
    },{
        "code": requests.codes.forbidden,
        "exception_class": FeatureUnavailableException
    },{
        "code": requests.codes.unauthorized,
        "exception_class": UnauthorizedAccessException
    }]

def test_raises_exceptions_correctly():
    for exception in response_exceptions:
        r = Response()
        r.status_code = exception["code"]
        try:
            raise_on_response(r)
            assert False
        except exception["exception_class"]:
            assert True