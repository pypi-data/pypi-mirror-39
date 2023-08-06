class RestException(BaseException):
    def __init__(self, message=None, status_code=None) -> None:
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"RestException: {self.message}"


class ValidationException(BaseException):
    def __init__(self, message=None) -> None:
        self.message = message

    def __str__(self):
        return f"ValidationException: {self.message}"


class BadRequest(RestException):
    def __init__(self, message=None, status_code=None) -> None:
        super().__init__(message, status_code)
        self.status_code = 400


class MethodNotAllowed(RestException):
    def __init__(self, message=None, status_code=None) -> None:
        super().__init__(message, status_code)
        self.status_code = 405

