from middleware import Middleware
from errors import AppException


class DefaultMiddleware(Middleware):
    def process_request(self, req):
        print(f"\n[REQUEST][{req.method}] {req.url}")

    def process_response(self, req, res):
        print(f"\n[RESPONSE] {req.url}")


class DefaultExceptionHandler:
    def __init__(self, app):
        self.app = app

    def handle_error(self, request, response, error):
        response.status_code = 500
        response.body = self.app.template(
            "error-500.html", context={"error": str(error)})
