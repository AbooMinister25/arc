from arc.defaults import DefaultExceptionHandler
from arc.staticfiles import StaticFile
from jinja2.loaders import FileSystemLoader
from jinja2 import Environment, FileSystemLoader
import os


class Collection:
    def __init__(self, templates_dir="templates", static_dir="static", exception_handler=None, host="127.0.0.1", port=5000):
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
        
        self.static_app = StaticFile(static_dir)
        
        self.add_route("/static/{filename}", self.static_app)

    def route(self, path):

        assert path not in self.routes, f"Route {path} already exists"

        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def add_route(self, path, handler):
        assert path not in self.routes, f"Route {path} already exists"

        self.routes[path] = handler

    def change_template_env(self, templates_dir):
        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir)))
        self.templates_dir = templates_dir

