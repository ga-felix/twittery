# General API Exception. Any API exception can be caught from it.
class ApiError(Exception):
    
    def __init__(self, message="Twitter API returned error code {}", code=000):
        if code != 000:
            self.message = message.format(code)
        else:
            self.message = message
        super().__init__(self.message)

# Rate Limit API exception code 429
class RateLimitError(ApiError):

    def __init__(self, message="Rate limit have been exhausted for the resource."):
        super().__init__(message=message)

# Forbidden API exception code 403
class ForbiddenError(ApiError):

    def __init__(self, message="Request was actively refused by API."):
        super().__init__(message=message)

# Not Found API exception code 404
class NotFoundError(ApiError):

    def __init__(self, message="Endpoint was not found."):
        super().__init__(message=message)

# Exception handler
def raiseError(code):
    if code == 429:
        raise RateLimitError()
    if code == 403:
        raise ForbiddenError()
    if code == 404:
        raise NotFoundError()
    raise ApiError(code=code)