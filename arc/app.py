from webob import Request, Response
from cheroot.wsgi import Server
from parse import parse
import socket


class App:
    def __init__(self):
        self.routes = {}
        self.host = "127.0.0.1"
        self.port = 5000

        self.server = Server(
            bind_addr=(self.host, self.port),
            wsgi_app=self,
            request_queue_size=500,
            server_name=socket.gethostname()
        )

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = f"Error 404, specified path not found on server"

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def route(self, path):
        
        assert path not in self.routes, f"Route {path} already exists"
        
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def run(self):
        try:
            print(f"[INFO] Running on http://{self.host}:{self.port}")
            print(f"[INFO] Press CTRL + C to stop")
            self.server.start()
        except KeyboardInterrupt:
            print(f"[INFO] Exiting Application")
            self.server.stop()
