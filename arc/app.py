from arc.middleware import Middleware
from arc.defaults import LoggingMiddleware, DefaultExceptionHandler
from arc.staticfiles import StaticFile
from arc.logger import Logger
import uvicorn
from parse import parse
import traceback
import inspect


class App:
    """
    The base App object. This object creates a WSGI application, and is used as the base object for creating routes, views, 
    templating, and more. Basic usage is as the following:: 

    from arc import App, TextResponse

    app = App()

    @app.route("/")
    def index(request):
        return TextResponse("Hello, World")

    if __name__ == "__main__":
        app.run()

    The app has several parameters.

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

    ..logging
        This parameter specifies whether the apps default logger should be activated. It can
        be deactivated as the following::

        app = App(logging=False)

    ..logger
        If the default logger is enabled, it specifies the logger the app should use.
        It can be changed as the following::

        app = App(logger=MyCustomLogger())
    """

    def __init__(self, static_dir: str = "static", exception_handler=None, host: str = "127.0.0.1", port: int = 5000, logging: bool = True, logger=Logger()):
        self.routes = {}

        # The host
        self.host = host

        # The port
        self.port = port

        if exception_handler is None:
            self.exception_handler = DefaultExceptionHandler(self)
        else:
            self.exception_handler = exception_handler()

        self.middleware = Middleware(self)

        if logging:
            self.add_middleware(LoggingMiddleware)

        self.static_app = StaticFile(static_dir)

        self.collections = []

        self.add_route("/static/{filename}", self.static_app)

        self.logger = logger

    async def __call__(self, scope, receive, send):
        await self.middleware(scope, receive, send)

    async def handle_request(self, request):
        handler, kwargs = self.find_handler(request_path=request.url.path)

        try:
            if handler is not None:

                if inspect.iscoroutinefunction(handler):
                    response = await handler(request, **kwargs)

                else:
                    response = handler(request, **kwargs)
            else:
                return self.default_response(request)

        except Exception as e:
            error = traceback.format_exc()
            response = self.exception_handler.handle_error(request, error)

        return response

    def default_response(self, request):
        return self.exception_handler.handle_404(request)

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def route(self, path: str):

        assert path not in self.routes, f"Route {path} already exists"

        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def add_route(self, path, handler):
        assert path not in self.routes, f"Route {path} already exists"

        self.routes[path] = handler

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)

    def to_seconds(self, time: int, type) -> int:
        if type.lower() not in ["hour", "minute"]:
            raise ValueError("Invalid type given")

        if type.lower() == "hour":
            return time * 60
        elif type.lower() == "minute":
            return time * 3600

    def register_collection(self, collection):
        assert collection not in self.collections, f"Collection {collection} already registered"
        for path in collection.routes.keys():
            assert path not in self.routes, f"Route {path} already exists"

            self.routes[path] = collection.routes[path]

        self.routes.update(collection.routes)
        self.collections.append(collection)

    def run(self, host: str = None, port: int = None, uvicorn_log_level="critical", reload=False, workers=1, access_log=True) -> None:
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port

        self.logger.log(f"Running on http://{self.host}:{self.port}", "info")
        self.logger.log(f"Press CTRL + C to stop", "info")
        uvicorn.run(self, host=self.host, port=self.port,
                    log_level=uvicorn_log_level, reload=reload, workers=workers, access_log=access_log)
        self.logger.log("Exiting Application", "critical")
