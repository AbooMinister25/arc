from arc.middleware import Middleware
from arc.defaults import DefaultMiddleware, DefaultExceptionHandler, TestClass
from jinja2.loaders import FileSystemLoader
from webob import Request, Response
from cheroot.wsgi import Server
from parse import parse
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
import socket
import inspect
import os
import traceback
import sys


class App:
    def __init__(self, templates_dir="templates", static_dir="static", exception_handler=None):
        self.routes = {}
        self.host = "127.0.0.1"
        self.port = 5000
        
        self.templates_dir = templates_dir

        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(self.templates_dir)))

        if exception_handler is None:
            self.exception_handler = DefaultExceptionHandler(self)
        else:
            self.exception_handler = exception_handler()

        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)

        self.middleware = Middleware(self)

        self.add_middleware(DefaultMiddleware)

        self.server = Server(
            bind_addr=(self.host, self.port),
            wsgi_app=self,
            request_queue_size=500,
            server_name=socket.gethostname()
        )

    def wsgi_app(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]

        if path_info.startswith("/static") or path_info.startswith("static"):
            environ["PATH_INFO"] = path_info[len("/static"):]
            return self.whitenoise(environ, start_response)

        return self.middleware(environ, start_response)

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        try:
            if handler is not None:
                if inspect.isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError(
                            "Method not allowed", request.method)

                handler(request, response, **kwargs)
            else:
                self.default_response(response)

        except Exception as e:
            error = traceback.format_exc()
            self.exception_handler.handle_error(request, response, error)

        return response

    def default_response(self, response):
        response.status_code = 404
        response.body = self.template("error-404.html")

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def route(self, path):

        assert path not in self.routes, f"Route {path} already exists"

        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def add_route(self, path, handler):
        assert path not in self.routes, f"Route {path} already exists"

        self.routes[path] = handler

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context).encode()

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)

    def run(self):
        try:
            print(f"[INFO] Running on http://{self.host}:{self.port}")
            print(f"[INFO] Press CTRL + C to stop")
            self.server.start()
        except KeyboardInterrupt:
            print("\n")
            print(f"[INFO] Exiting Application")
            self.server.stop()
