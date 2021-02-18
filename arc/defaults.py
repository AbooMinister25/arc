from arc.middleware import Middleware
from arc.errors import AppException
import os


class DefaultMiddleware(Middleware):
    def process_request(self, req):
        print(f"\n[REQUEST][{req.method}] {req.url}")

    def process_response(self, req, res):
        print(f"\n[RESPONSE] {req.url}")


class DefaultExceptionHandler:
    def __init__(self, app):
        self.app = app
        app.templates_dir = os.path.abspath("selfpages")

    def handle_error(self, request, response, error):
        response.status_code = 500
        response.body = self.app.template(
            "error-500.html", context={"error": str(error)})

class TestClass:
    def __init__(self):
        self.test()
    def test(self):
        print("TEST")