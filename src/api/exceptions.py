class ApiException(Exception):
    pass

class RateLimit(ApiException):

    def __init__(self,  message="Rate limit have been exhausted. Error code 429."):
        self.message = message
        super().__init__(self.message)

class Forbidden(ApiException):

    def __init__(self,  message="Access was refused. Error code 403."):
        self.message = message
        super().__init__(self.message)

class NotFound(ApiException):

    def __init__(self,  message="Access was refused. Error code 404."):
        self.message = message
        super().__init__(self.message)