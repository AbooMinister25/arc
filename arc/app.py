from arc.middleware import Middleware
from arc.defaults import DefaultMiddleware, DefaultExceptionHandler
from jinja2.loaders import FileSystemLoader
from starlette.requests import Request
import uvicorn
from parse import parse
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
import socket
import inspect
import os
import traceback


class App:
    """
    The base App object. This object creates a WSGI application, and is used as the base object for creating routes, views, 
    templating, and more. Basic usage is as the following:: 

    from arc import App

    app = App("app")

    @app.route("/")
    def index(req, res):
        res.text = 'Hello, World'

    if __name__ == "__main__":
        app.run()

    The app has several parameters.

    ..name ::
        This paramter is used to specifiy the apps name. It is required, and has to be the same as the variable name
        you assigned the App class to.

        app = App("app")


    ..templates_dir ::
        This parameter is used to specify the directory that jinja loads its HTML templates from. Its defaulted to 
        the 'templates' directory, but you can change it as the following::

        app = App(templates_dir="public")

    ..static_dir ::
        This parameter is used to specify the directory that static files are served from. Its defaulted to the
        'static' folder. You can change it as the following::

        app = App(static_dir="css")

    ..exception_handler ::
        This parameter is used to specify a custom exception handler for the app to use instead of the default
        one. It uses the base AppException class. It's defaulted to None, which causes the app to use the
        default exception handler. It can be changed as the following::

        app = App(exception_handler=CustomExceptionHandler)

    ..host ::
        This parameter is used to specify the host that the app will run on. Its defaulted 
        to '127.0.0.1'. It can be changed as the following::

        app = App(host="181.177.121.773")

    ..port ::
        This parameter is used to specify which port the app will listen on. Its defaulted to 
        port `5000`. You can change it as the following::

        app = App(port=8000)

    ..default_middleware
        This parameter specifies whether the app should use the default middleware, which logs requests and
        responses into the console. Its set to True by default. You can change it as the following::

        app = App(default_middleware=False)
    """

    def __init__(self, templates_dir="templates", static_dir="static", exception_handler=None, host="127.0.0.1", port=5000, default_middleware=True):
        self.routes = {}

        # The host
        self.host = host

        # The port
        self.port = port

        self.templates_dir = templates_dir

        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(self.templates_dir)))

        if exception_handler is None:
            self.exception_handler = DefaultExceptionHandler(self)
        else:
            self.exception_handler = exception_handler()

        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)

        self.middleware = Middleware(self)

        if default_middleware:
            self.add_middleware(DefaultMiddleware)

        self.collections = []

    async def wsgi_app(self, scope, recieve, send):
        request = Request(scope, recieve=recieve)

        response = self.handle_request(request)

        await response(scope, recieve, send)

    async def __call__(self, scope, recieve, send):
        path_info = scope["path"]

        # if path_info.startswith("/static") or path_info.startswith("static"):
        #     scope["PATH_INFO"] = path_info[len("/static"):]
        #     return self.whitenoise(environ, start_response)

        await self.middleware(scope, recieve, send)

    def handle_request(self, request):
        handler, kwargs = self.find_handler(request_path=request.url.path)

        try:
            if handler is not None:
                if inspect.isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError(
                            "Method not allowed", request.method)

                response = handler(request, **kwargs)
            else:
                self.default_response()

        except Exception as e:
            error = traceback.format_exc()
            response = self.exception_handler.handle_error(error)

        return response

    def default_response(self):
        self.exception_handler.handle_404()

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

    def custom_template(self, templates_path, template_name, context=None):
        if context is None:
            context = {}

        return Environment(loader=FileSystemLoader(templates_path)).get_template(template_name).render(**context).encode()

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)

    def change_template_env(self, templates_dir):
        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir)))
        self.templates_dir = templates_dir

    def set_cookie(self, key, value, resp, lifetime=None, secure=False):
        if lifetime is not None:
            resp.set_cookie(key, value, secure=secure)
        else:
            resp.set_cookie(
                key, value, max_age=lifetime, secure=secure)

    def get_cookies(self, req):
        return req.cookies

    def get_cookie(self, key, req):
        return dict(req.cookies)[key]

    def register_collection(self, collection):
        assert collection not in self.collections, f"Collection {collection} already registered"
        collection.set_wsgi(self.wsgi_app)
        for path in collection.routes.keys():
            assert path not in self.routes, f"Route {path} already exists"

            self.routes[path] = collection.routes[path]

        self.routes.update(collection.routes)
        self.collections.append(collection)

    def run(self):
        print(f"[INFO] Running on http://{self.host}:{self.port}")
        print(f"[INFO] Press CTRL + C to stop")
        uvicorn.run(self, host="127.0.0.1", port=5000,
                    log_level="critical")
