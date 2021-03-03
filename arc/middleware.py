from starlette.requests import Request
import inspect


class Middleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        request = Request(scope=scope, receive=receive)

        response = await self.app.handle_request(request)

        await response(scope, receive, send)

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
