from typing import Optional, Union
from arc.types import CoroutineFunction


class Request:
    def __init__(
        self, scope: dict, receive: CoroutineFunction, send: CoroutineFunction
    ):
        if scope["type"] != "http":
            raise ValueError("Type of request must be http")

        self.scope = scope
        self._receive = receive
        self._send = send


