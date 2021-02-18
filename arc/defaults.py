from arc.middleware import Middleware
from arc.errors import AppException
import os
import pathlib
from jinja2 import Environment, FileSystemLoader
from jinja2.loaders import FileSystemLoader


class DefaultMiddleware(Middleware):
    def process_request(self, req):
        print(f"\n[REQUEST][{req.method}] {req.url}")

    def process_response(self, req, res):
        print(f"\n[RESPONSE] {req.url}")


class DefaultExceptionHandler:
    def __init__(self, app):
        self.app = app
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(self.dir_path, "selfpages")
        self.errors_env = Environment(
            loader=FileSystemLoader(os.path.join(self.dir_path, "selfpages")))

    def handle_error(self, request, response, error):
        response.status_code = 500
        response.body = self.errors_env.get_template(
            "error-500.html").render({"error": error}).encode()

    def handle_404(self, response):
        response.status_code = 404

        response.body = self.errors_env.get_template(
            "error-404.html").render().encode()
