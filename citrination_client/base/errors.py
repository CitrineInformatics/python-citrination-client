class CitrinationClientError(Exception):

    def __init__(self, message=None, server_response=None):
        if message is not None and server_response is not None:
            message = "{}\nCitrination returned: {}".format(message, server_response)
        super(CitrinationClientError, self).__init__(message)

class APIVersionMismatchException(CitrinationClientError):

    def __init__(self, message="Version mismatch with Citrination identified, server_response=None. Please check for available PyCC updates", server_response=None):
        super(APIVersionMismatchException, self).__init__(message)

class FeatureUnavailableException(CitrinationClientError):

    def __init__(self, message="This feature is unavailable on your Citrination deployment", server_response=None):
        super(FeatureUnavailableException, self).__init__(message)

class UnauthorizedAccessException(CitrinationClientError):

    def __init__(self, message="Access to an unauthorized resource requested", server_response=None):
        super(UnauthorizedAccessException, self).__init__(message)

class ResourceNotFoundException(CitrinationClientError):

    def __init__(self, message="Resource not found", server_response=None):
        super(ResourceNotFoundException, self).__init__(message)

class CitrinationServerErrorException(CitrinationClientError):

    def __init__(self, message=None, server_response=None):
        super(CitrinationServerErrorException, self).__init__(message)

class RequestTimeoutException(CitrinationClientError):

    def __init__(self, message="Request to Citrination host timed out", server_response=None):
        super(RequestTimeoutException, self).__init__(message)

class RateLimitingException(CitrinationClientError):

    def __init__(self, message="Rate limit hit, throttle requests", server_response=None):
        super(RateLimitingException, self).__init__(message)
