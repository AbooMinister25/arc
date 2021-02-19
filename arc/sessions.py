

class Session:
    def __init__(self, app):
        self.app = app
        self._dict = {}
    
    def __setitem__(self, key, value):
        self.app.set_cookie(key, value)
        self._dict[key] = value
    
    def __getitem__(self, key):
        return self._dict[key]