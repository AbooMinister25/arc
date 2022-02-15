from typing import Optional, Union
import http


class ArcException(Exception):
    """Used to represent exceptions in an Arc application.

    Args:
        message: An message which contains details related to
          the error.
        status_code: The status code for the error.
    """

    def __init__(
        self,
        message: Optional[Union[str, bytes]] = None,
        status_code: Optional[int] = None,
    ):
        self.message = (
            message or http.HTTPStatus(status_code) if status_code is not None else ""
        )  # Use the provided message, or fetch one based on a given status code, if any

        if status_code is not None:
            self.status_code = status_code

        super().__init__(message)


class PageNotFound(ArcException):
    """404 exception, page not found"""

    status_code = 404

    def __init__(
        self,
        message: Optional[Union[str, bytes]] = None,
    ):
        super().__init__(message, self.status_code)


class InternalServerError(ArcException):
    """500 exception, internal server error"""

    status_code = 500

    def __init__(
        self,
        message: Optional[Union[str, bytes]] = None,
    ):
        super().__init__(message, self.status_code)


class MethodNotAllowed(ArcException):
    """405 exception, method not allowed"""

    status_code = 405

    def __init__(
        self,
        message: Optional[Union[str, bytes]] = None,
    ):
        super().__init__(message, self.status_code)


class BadRequest(ArcException):
    """400 exception, bad request"""

    status_code = 400

    def __init__(
        self,
        message: Optional[Union[str, bytes]] = None,
    ):
        super().__init__(message, self.status_code)


class MissingQueryParameter(ArcException):
    """422 exception, unprocessable entity"""

    status_code = 422

    def __init__(
        self,
        message: Optional[Union[str, bytes]] = None,
    ):
        super().__init__(message, self.status_code)


class Forbidden(ArcException):
    """403 exception, forbidden"""

    status_code = 403

    def __init__(
        self,
        message: Optional[Union[str, bytes]] = None,
    ):
        super().__init__(message, self.status_code)
