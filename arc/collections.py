from arc.defaults import DefaultExceptionHandler
import os


class Collection:
    def __init__(self, templates_dir="templates", static_dir="static", exception_handler=None, host="127.0.0.1", port=5000):
        self.routes = {}

        # The host
        self.host = host

        # The port
        self.port = port

        self.templates_dir = templates_dir

        if exception_handler is None:
            self.exception_handler = DefaultExceptionHandler(self)
        else:
            self.exception_handler = exception_handler()


    def route(self, path):

        assert path not in self.routes, f"Route {path} already exists"

        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def add_route(self, path, handler):
        assert path not in self.routes, f"Route {path} already exists"

        self.routes[path] = handler

