from starlette.requests import Request
from starlette.websockets import WebSocket
import inspect
import traceback


class Middleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            if scope["type"] == "http":
                request = Request(scope=scope, receive=receive)

                response = await self.app.handle_request(request)

            elif scope["type"] == "websocket":
                websocket = WebSocket(scope=scope, receive=receive, send=send)

                response = await self.app.handle_request(websocket)

            await response(scope, receive, send)
        except:
            error = traceback.format_exc()
            print(error)
            response = self.exception_handler.handle_error(request, error)

    def add(self, middleware_cls, *args):
        if args == []:
            args = None
        self.app = middleware_cls(self.app, *args)

    async def process_request(self, req):
        pass

    async def process_response(self, req, res):
        pass

    async def handle_request(self, request):
        if inspect.iscoroutinefunction(self.process_request):
            await self.process_request(request)
        else:
            self.process_response(request)

        response = await self.app.handle_request(request)

        if inspect.iscoroutinefunction(self.process_response):
            await self.process_response(request, response)
        else:
            self.process_response(request, response)

        return response
