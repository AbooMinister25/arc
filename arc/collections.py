class Collection:
    def __init__(self):
        self.routes = {}

    def route(self, path: str, methods=["GET", "POST", "HEAD", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]):

        assert path not in self.routes, f"Route {path} already exists"

        for method in methods:
            assert method in ["GET", "POST", "HEAD", "PUT", "DELETE", "CONNECT",
                              "OPTIONS", "TRACE", "PATCH"], f"Method {method} doesn't exist"

        def wrapper(handler):
            self.add_route(path, handler, methods)
            return handler

        return wrapper

    def add_route(self, path, handler, methods=["GET", "POST", "HEAD", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]):
        assert path not in self.routes, f"Route {path} already exists"

        self.routes[path] = {"handler": handler,
                             "methods": methods}

    def websocket(self, path: str):
        assert path not in self.routes, f"Route {path} already exists"

        def wrapper(handler):
            self.add_websocket(path, handler)
            return handler

        return wrapper

    def add_websocket(self, path, handler):
        assert path not in self.routes, f"Route {path} already exists"

        self.routes[path] = {"handler": handler}

    def to_seconds(self, time: int, type) -> int:
        if type.lower() not in ["hour", "minute"]:
            raise ValueError("Invalid type given")

        if type.lower() == "hour":
            return time * 60
        elif type.lower() == "minute":
            return time * 3600
