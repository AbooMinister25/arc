from starlette.requests import Request
import secrets


class SessionHandler:
    def __init__(self, app, lifetime=None, secret_key=None):
        self.app = app
        
        if lifetime is None:
            self.lifetime = self.app.to_seconds(1, "hour")
        else:
            lifetime = self.lifetime

        self.secret_key = secrets.token_urlsafe()

        self.initialized = False

    def init_session(self, request, response):
        if not request.cookies.get("secret_key"):
            key = secrets.token_urlsafe(50)
            response.set_cookie("secret_key", key+self.secret_key,
                                httponly=True, max_age=self.lifetime)

            self._dict = {}

            self.initialized = True

            self.app.config["SECRET_KEY"] = key+self.secret_key
            self.app.config["SESSION"] = {}

            return

        if request.cookies.get("secret_key") == self.app.config["SECRET_KEY"]:
            self.initialized = True
        else:
            raise ValueError("Invald Secret Key")

    def __call__(self):
        assert self.initialized, "Session Not Initialized"
        return self.app.config["SESSION"]
