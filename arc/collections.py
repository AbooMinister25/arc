from arc.defaults import DefaultExceptionHandler
from jinja2.loaders import FileSystemLoader
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
import os


class Collection:
    def __init__(self, templates_dir="templates", static_dir="static", wsgi_app=None):
        self.routes = {}

        self.templates_dir = templates_dir
        self.static_dir = static_dir

        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(self.templates_dir)))

        self.whitenoise = WhiteNoise(wsgi_app, root=static_dir)

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

    def set_wsgi(self, wsgi):
        self.whitenoise = WhiteNoise(wsgi, root=self.static_dir)
