from citrination_client.errors import CitrinationClientError

class APIVersionMismatchException(CitrinationClientError):

  def __init__(self, message="Version mismatch with Citrination identified. Please check for available PyCC updates"):
      super(APIVersionMismatchException, self).__init__(message)

class FeatureUnavailableException(CitrinationClientError):

  def __init__(self, message="Access to an unauthorized resource requested"):
      super(FeatureUnavailableException, self).__init__(message)

class UnauthorizedAccessException(CitrinationClientError):

  def __init__(self, message="Access to an unauthorized resource requested"):
      super(UnauthorizedAccessException, self).__init__(message)

class CitrinationServerErrorException(CitrinationClientError):

  def __init__(self, message=None):
      super(CitrinationServerErrorException, self).__init__(message)
