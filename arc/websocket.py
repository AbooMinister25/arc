import websockets
import asyncio
from starlette.requests import HTTPConnection, empty_receive, empty_send


class WebSocket(HTTPConnection):
    def __init__(self, scope, recieve=empty_receive, send=empty_send):
        super().__init__(scope)
        
        self._recieve = recieve 
        self._send = send
        
        assert scope["type"] == "websocket"
    
