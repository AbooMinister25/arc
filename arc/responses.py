from starlette.responses import Response
from urllib.parse import quote_plus
import typing
import orjson


class TextResponse(Response):
    media_type = "text/plain"


class Redirect(Response):
    def __init__(self, url: str, status_code: int = 307, headers: dict = None) -> None:
        super().__init__(
            content=b"", status_code=status_code, headers=headers
        )
        self.headers["location"] = quote_plus(
            str(url), safe=":/%#?&=@[]!$&'()*+,;")


class JSON(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(
            content
        )


class HTML(Response):
    media_type = "text/html"
