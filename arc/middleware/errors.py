from typing import Optional, Callable

from arc.types import CoroutineFunction
from arc.exceptions import (
    ArcException,
)
from arc.http import HTTPResponse, HTMLResponse

HTML_RESPONSE_TEMPLATE = """
<html>
    <h1> Error {} </h1>
    <p>{}</p>
    
    <div class="traceback">
        
    </div>
</html>
"""


async def base_exception_handler(
    message: str, status_code: int, response_type: str
) -> HTTPResponse:
    if response_type == "html":
        return HTMLResponse(
            """
            
            """
        )


class ExceptionMiddleware:
    def __init__(
        self,
        app: CoroutineFunction,
        debug: Optional[bool] = False,
        response_type: Optional[str] = "html",
    ):
        self.app = app
        self.debug = debug

        if response_type.lower() not in ("html", "text", "json"):
            raise AttributeError(
                f"Response type {response_type} invalid, has to be one of html, text, or json"
            )

        self.response_type = response_type.lower()

    def build_exception_handler(self) -> dict[Exception, Callable]:
        ...

    async def http_exception(self, status_code: int) -> HTTPResponse:
        ...

    async def __call__(
        self, scope: dict, receive: CoroutineFunction, send: CoroutineFunction
    ):
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            if isinstance(e, ArcException):
                if e.status_code is not None:
                    await self.http_exception(e.status_code)
                else:
                    await self.default_exception()
