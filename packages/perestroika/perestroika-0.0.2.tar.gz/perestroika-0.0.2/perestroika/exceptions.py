class RestException(BaseException):
    def __init__(self, message=None, status_code=None) -> None:
        self.message = message
        self.status_code = status_code


class ValidationException(BaseException):
    def __init__(self, message=None) -> None:
        self.message = message


class BadRequest(RestException):
    status_code = 400


class MethodNotAllowed(RestException):
    status_code = 405

