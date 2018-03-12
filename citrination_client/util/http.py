from citrination_client.errors import CitrinationClientError

def get_success_json(response, failure_message):
    if response.status_code != 200:
        raise CitrinationClientError(
            "{} - Citrination returned {}".format(failure_message, response.status_code)
        )

    return response.json()