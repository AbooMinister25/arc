import orjson


class JSONRouteLoader:
    def __init__(self, file):
        with open(file, "r") as routes_file:
            routes_dict = orjson.load(routes_file.read())
        
        self.routes = {}
        
        for route, handler in routes_dict.items():
            self.routes[route] = handler
        
        