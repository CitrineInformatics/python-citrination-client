from citrination_client.errors import CitrinationClientError

def get_success_json(response, failure_message="Unsuccessful request to Citrination"):
    return get_response_json(check_success(response, failure_message))

def check_success(response, failure_message):
    if response.status_code >= 300:
        raise CitrinationClientError(
            "{} - Citrination returned {}".format(failure_message, response.status_code)
        )
    return response

def get_response_json(response):
    return response.json()