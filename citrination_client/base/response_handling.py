from errors import *
from time import sleep

def check_for_rate_limiting(response, response_lambda, timeout=0, attempts=0):
    if attempts >= 3:
        raise RateLimitingException()
    if response.status_code == 429:
        sleep(timeout)
        new_timeout = timeout + 1
        new_attempts = attempts + 1
        return check_for_rate_limiting(response_lambda(timeout, attempts), response_lambda, timeout=new_timeout, attempts=new_attempts)
    return response

def check_general_success(response, failure_message):
    if response.status_code >= 400:
        raise CitrinationClientError(
            "{} - Citrination returned {}".format(failure_message, response.status_code)
        )
    return response

def get_response_json(response):
    return response.json()

def raise_on_response(response):
    _check_response_for_version_mismatch(response)
    _check_response_for_feature_availability(response)
    _check_response_for_authorization(response)
    _check_response_for_timeout(response)
    _check_response_for_server_error(response)
    return response

def _check_response_for_authorization(response):
    if response.status_code == 401:
        raise UnauthorizedAccessException()

def _check_response_for_feature_availability(response):
    if response.status_code == 403:
        raise FeatureUnavailableException()

def _check_response_for_timeout(response):
    if response.status_code == 524:
        raise RequestTimeoutException()

def _check_response_for_server_error(response):
    if response.status_code >= 500:
        raise CitrinationServerErrorException(
                "Citrination returned an error code - code: {}, body: {}".format(response.status_code, response.content)
            )

def _check_response_for_version_mismatch(response):
    try:
        if response.status_code == 400:
            error_type = response_content["error_type"]
            if error_type == "Version Mismatch":
                raise APIVersionMismatchException()
        return response
    except KeyError:
        return response