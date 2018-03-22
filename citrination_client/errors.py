class CitrinationClientError(Exception):
  pass

class RequestTimeoutException(CitrinationClientError):

  def __init__(self, message="Request to Citrination timed out"):
    super(RequestTimeoutException, self).__init__(message)