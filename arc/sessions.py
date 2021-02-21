

class Session:
    def __init__(self, app, lifetime="session"):
        self.app = app
        self._dict = {}
        self.lifetime = lifetime

    def __getitem__(self, key):
        return self._dict[key]

    def make_session(self, key, value, resp):
        if self.lifetime == "session":
            self.app.set_cookie(key, value, resp)
        else:
            self.app.set_cookie(key, value, resp, lifetime=self.lifetime)

        self._dict[key] = value
