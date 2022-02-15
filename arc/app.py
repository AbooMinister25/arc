from typing import Optional, Sequence, TypeVar, Type

import uvicorn

from arc.routing import Route, Router
from arc.types import CoroutineFunction, DCallable, Callable

T = TypeVar("T")


class Arc:
    """The main ASGI application

    An ASGI application.

    Args:
        routes: A sequence of routes that the Arc application will
          use.
        middleware: A sequence of objects that are used as the middleware
          for the ASGI app.

    Attributes:
        router: The router for the ASGI app.
        middleware: The middleware for the ASGI app.
    """

    def __init__(
        self,
        *,
        routes: Optional[Sequence[Route]] = None,
        middleware: Optional[Sequence[tuple[Type[T], dict]]] = None,
    ):
        self.router = Router(self, routes)

        self.middleware = (
            self.router
        )  # Set the initial middleware app to the app's router

        if middleware is not None:
            for cls, args in reversed(middleware):
                self.middleware = cls(**args)

    async def __call__(
        self, scope: dict, receive: CoroutineFunction, send: CoroutineFunction
    ):
        await self.router(scope, receive, send)

    def route(self, path: str, methods: Optional[Sequence[str]]) -> DCallable:
        """A decorator used for adding new routes to the application's Router.

        A wrapper around the application's Router's `register` function that
        is used as a decorator.

        Args:
            path: The path for the route.
            methods: A sequence of HTTP methods that the route should accept.

        Returns:
            A decorated callable function.
        """

        def wrapper(handler: Callable):
            self.router.register(path, handler, methods)
            return handler

        return wrapper

    def run(self):
        uvicorn.run(self, host="127.0.0.1", port=5000)
