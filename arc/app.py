from typing import Optional, Sequence

import uvicorn

from arc.router import Route, Router
from arc.types import CoroutineFunction


class Arc:
    """
    The main application class

    :param routes: A sequence of routes for the app to use.
    """

    def __init__(self, *, routes: Optional[Sequence[Route]] = None):
        self.router = Router(self, routes)

    async def __call__(
        self, scope: dict, receive: CoroutineFunction, send: CoroutineFunction
    ):
        await self.router(scope, receive, send)

    def run(self):
        uvicorn.run(self, host="127.0.0.1", port=5000)
