from arc.middleware import Middleware
from arc.errors import AppException
from arc.templates import Template
import os
import logging



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
        self.template = Template(self.path)

    def handle_error(self, request, error: str):
        return self.template("error-500.html", context={"request": request, "error": error})

    def handle_404(self, request):
        return self.template("error-404.html", context={"request": request})