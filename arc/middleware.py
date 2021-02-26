from starlette.requests import Request

class Middleware:
    def __init__(self, app):
        self.app = app
        self.test = "YAY"
    
    async def __call__(self, scope, receive, send):
        request = Request(scope=scope, receive=receive)
        
        response = self.app.handle_request(request)
        
        await response(scope, receive, send)
        return response(scope, receive, send)

    def add(self, middleware_cls):
        self.app = middleware_cls(self.app)

    def process_request(self, req):
        pass

    def process_response(self, req, res):
        pass

    def handle_request(self, request):
        self.process_request(request)

        response = self.app.handle_request(request)
        self.process_response(request, response)

        return response


