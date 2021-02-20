

class Session:
    def __init__(self, app, lifetime="session"):
        self.app = app
        self._dict = {}
        self.lifetime = lifetime
    
    def __setitem__(self, key, value):
        if self.lifetime == "session":
            self.app.set_cookie(key, value)
        else:
            self.app.set_cookie(key, value, lifetime=self.lifetime)
        self._dict[key] = value
    
    def __getitem__(self, key):
        return self._dict[key]