from typing import Any, Optional, Union

import orjson

from arc.types import CoroutineFunction


class HTTPResponse:
    """Base HTTP response object

    Provides the common functionality between all the other
    HTTP response classes.

    Args:
        body: The body of the response, can be either
          bytes or a string
        status_code: The status code of the response,
          defaults to 200.
        headers: A dictionary which represents the HTTP
          headers for the response.

    Attributes:
        body: The body of the response, is either bytes
          or a string.
        status_code: The status code of the response.
        headers: A dictionary which represents the HTTP
          headers for the response.
    """

    content_type: Optional[str] = None

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
        self.headers = headers or {}
        if content_type is not None:
            self.headers["content-type"] = content_type

    @property
    def raw_headers(self) -> list[tuple[bytes, bytes]]:
        """A list of raw header values

        Returns:
            A list of tuples which contain bytes.
        """
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
    """HTTP response with the content being JSON

    Takes and serializes the given JSON using `orjson`.

    Args:
        data: The JSON data for the response to use.

    Attributes:
        body: The serialized form of the JSON provided to
          the response.
    """

    def __init__(self, data: Any, *args, **kwargs):
        body = orjson.dumps(data)

        super().__init__(
            body,
            content_type="application/json",
            *args,
            **kwargs,
        )


class HTMLResponse(HTTPResponse):
    """HTTP response with the content being HTML"""

    content_type = "text/html"
