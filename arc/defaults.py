from arc.middleware import Middleware
from arc.templates import Template
import os


class LoggingMiddleware(Middleware):
    async def process_request(self, req):
        try:
            self.app.logger.log(f"[REQUEST][{req.method}] {req.url}", "info")
        except AttributeError:
            self.app.logger.log(f"[WEBSOCKET][{req.url}]", "info")

    async def process_response(self, req, res):
        self.app.logger.log(f"[RESPONSE] {req.url}", "info")


class DefaultExceptionHandler:
    def __init__(self, app):
        self.app = app
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(self.dir_path, "selfpages")
        self.template = Template(self.path)

    def handle_error(self, request, error: str):
        self.app.logger.log(error, "error")
        return self.template("error-500.html", context={"request": request, "error": error})

    def handle_404(self, request):
        self.app.logger.log(f"{request.url.path} not found", "error")
        return self.template("error-404.html", context={"request": request, "url": request.url.path})
