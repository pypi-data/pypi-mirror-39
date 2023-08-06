class RestException(BaseException):
    def __init__(self, message=None) -> None:
        self.message = message


class ValidationException(BaseException):
    def __init__(self, message=None) -> None:
        self.message = message


class BadRequest(RestException):
    status_code = 400


class MethodNotAllowed(RestException):
    status_code = 405

