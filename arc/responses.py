import json
from typing import Any, Optional, Union

from arc.types import CoroutineFunction


class HTTPResponse:
    """
    Base HTTP response object

    :param body: The body of the response object.
    :param status_code: The status code of the resonse, defaults to 200.
    :param headers: A dict of the headers for the response.
    """

    def __init__(
        self,
        body: Optional[Union[bytes, str]] = b"",
        *,
        status_code: Optional[int] = 200,
        headers: Optional[dict] = None,
        content_type: Optional[str] = None,
    ):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.body = body
        self.status_code = status_code
        self.headers = headers if headers is not None else {}
        if content_type is not None:
            self.headers["content-type"] = content_type

    @property
    def raw_headers(self) -> list[tuple[bytes, bytes]]:
        if self.headers is None:
            return []

        raw_headers = [
            (k.encode("latin-1"), v.encode("latin-1")) for k, v in self.headers.items()
        ]
        return raw_headers

    async def __call__(
        self, scope: dict, receive: CoroutineFunction, send: CoroutineFunction
    ):
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": self.body,
            }
        )


class JSONResponse(HTTPResponse):
    """
    JSON response class. Used for sending JSON responses

    :param data: The JSON data for the response to return.
    """

    def __init__(self, data: Any, *args, **kwargs):
        body = json.dumps(data)

        super().__init__(
            body,
            content_type="application/json",
            *args,
            **kwargs,
        )
