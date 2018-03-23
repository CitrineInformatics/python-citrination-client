from citrination_client.base.response_handling import raise_on_response, check_general_success, check_for_rate_limiting, _check_response_for_version_mismatch
from citrination_client.base.errors import *
from requests.models import Response
import requests
import json

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
    """
    Tests that the exceptions which map directly to a particular
    error code are thrown correctly in the raise_on_response method
    """
    for exception in response_exceptions:
        r = Response()
        r.status_code = exception["code"]
        try:
            raise_on_response(r)
            assert False
        except exception["exception_class"]:
            assert True

def test_check_response_for_version_mismatch():
    """
    Tests that the version mismatch check will throw an error
    if the error_type key is present with the right value in the
    JSON response
    """
    r = Response()
    r.status_code = requests.codes.bad
    # accesses library private variable, but not sure how to mock responses
    r._content = json.dumps({"error_type": "Version Mismatch"})
    try:
        _check_response_for_version_mismatch(r)
        assert False
    except APIVersionMismatchException:
        assert True

def test_check_response_for_version_mismatch_not_json():
    """
    Tests that the version mismatch test passes a response through
    if the content is not JSON parseable
    """
    r = Response()
    r.status_code = requests.codes.bad
    # accesses library private variable, but not sure how to mock responses
    r._content = "definitely not json"
    assert r is _check_response_for_version_mismatch(r)

def test_raises_client_error_if_error_code():
    """
    Tests that in the case of a generically bad response, a client
    exception is thrown
    """
    r = Response()
    r.status_code = requests.codes.bad
    try:
        check_general_success(r, "failure detected")
        assert False
    except CitrinationClientError:
        assert True

def test_if_rate_limiting_returns_on_resolve():
    """
    Tests that, if a rate limiting http code is returned and the
    client retries the request after sleeping and a success code is
    returned, no rate limiting exception will be raised
    """
    bad_response = Response()
    bad_response.status_code = 429
    good_response = Response()
    good_response.status_code = 200
    response_lambda = (lambda t, a: bad_response if a < 1 else good_response)
    try:
        check_for_rate_limiting(bad_response, response_lambda)
        assert True
    except RateLimitingException:
        assert False

def test_after_three_attempts_rate_limit_errors():
    """
    Tests that if three rate limiting error codes are encountered in a row (with backoff), a custom exception will be thrown
    """
    bad_response = Response()
    bad_response.status_code = 429
    response_lambda = (lambda t, a: bad_response)
    try:
        check_for_rate_limiting(bad_response, response_lambda)
        assert False
    except RateLimitingException:
        assert True

def test_success_does_not_trigger_rate_limiting_retry():
    """
    Tests that the retry lambda is not called if the original request is successful
    """
    response = Response()
    response.status_code = 200
    response_lambda = (lambda t, a: 1/0) # will throw exception
    checked_resp = check_for_rate_limiting(response, response_lambda)
    assert response == checked_resp