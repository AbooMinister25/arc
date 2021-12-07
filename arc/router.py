import inspect
import re
from typing import Any, Optional, Pattern, Sequence
from urllib.parse import parse_qs

from arc.errors import InvalidTypeError
from arc.responses import JSONResponse
from arc.types import CoroutineFunction, DCallable

METHODS = {
    "get",
    "post",
    "delete",
    "put",
    "head",
    "connect",
    "options",
    "trace",
    "patch",
}

PATH_REGEX = re.compile(
    r"{([a-zA-Z_][a-zA-Z\d_]*)}"
)  # The regex for matching path parameters in a url


def get_path_params(path: str) -> list[str]:
    """
    Returns a tuple of path parameters from a given path

    :param path: A string path that the function extracts the path parameters from
    :return: A list of strings which represent the path parameters
    """

    path_params = []

    for path in PATH_REGEX.finditer(path):
        param_name = path.group()[1:-1]  # The name of the path parameter
        path_params.append(param_name)

    return path_params


def compile_path_regex(path: str, path_params: list[str]) -> Pattern:
    """
    Returns a compiled regex for matching a given path

    :param path: A string path to generate a regex for
    :param path_params: A list of the path parameters in the path
    :return: A compiled regex pattern
    """

    new_path = path

    for param in path_params:
        new_path = new_path.replace(
            f"{{{param}}}", rf"(?P<{param}>[a-zA-Z_0-9]+)"
        )  # Replace the path parameter with a regex group for matching it

    return re.compile(new_path)


def parse_params(
    q_params: dict[str, Any],
    p_params: dict[str, Any],
    types: dict[str, type],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Function used to parse query and path parameters to their corresponding types

    :param q_params: A dictionary of query parameters and their values
    :param p_params: a dictionary of path parameters and their values
    :param types: A dictionary of the handler function's parameter typess
    :return: A tuple of two dicts which contain the parsed query and path parameters
    """

    parsed_q = {}  # Parsed query parameters
    parsed_p = {}  # Paresd path parameters

    for name, value in q_params.items():
        type_ = types.get(name)
        if type_ is None:
            # If the type wasn't declared for the parameter,
            # continue to the next iteration of the loop
            continue

        try:
            # Try to cast the parameter to the corresponding type, otherwise raise an error
            parsed_q[name] = type_(value)
        except ValueError:
            raise InvalidTypeError(
                f"Could not parse query parameter {name} to {type_.__name__}"
            )

    for name, value in p_params.items():
        type_ = types.get(name)
        if type_ is None:
            # If the type wasn't declared for the parameter,
            # continue to the next iteration of the loop
            continue

        try:
            # Try to cast the parameter to the corresponding type, otherwise raise an error
            parsed_p[name] = type_(value)
        except ValueError:
            raise InvalidTypeError(
                f"Could not parse query parameter {name} to {type_.__name__}"
            )

    return parsed_q, parsed_p


class Route:
    """
    The base Route class. Used for representing different
    routes in an Arc application.

    :param path: The path for the route.
    :param handler: An asynchronous function that is used as a handler for the route.
    :param methods: A sequence of methods that the route accepts.
    """

    def __init__(
        self,
        path: str,
        handler: CoroutineFunction,
        methods: Optional[Sequence[str]] = None,
    ):
        if not inspect.iscoroutinefunction(handler):
            raise AttributeError("Handler must be an asynchronous function")

        self.path = path
        self.handler = handler
        if methods:
            if not all(
                method.lower() in METHODS for method in methods
            ):  # If a given request method isn't in the global METHODS set, raise an error
                raise AttributeError("Invalid request methods provided")
        self.methods = methods
        self.path_params = get_path_params(path)  # Get the path parameters for the url
        self.path_regex = compile_path_regex(
            path, self.path_params
        )  # Get the path regex used for matching on the URL


class Router:
    """
    The Router class. Used for managing and dispatching routes for the main Arc application

    :param app: An ASGI application.
    :param routes: A sequence of Routes to pass into the router.
    """

    def __init__(
        self, app: CoroutineFunction, routes: Optional[Sequence[Route]] = None
    ):
        self.routes = list(routes) if routes is not None else []
        self.paths = [route.path for route in self.routes]
        self.app = app

    def register(
        self,
        path: str,
        handler: CoroutineFunction,
        methods: Optional[Sequence[str]] = None,
    ):
        """
        Registers a route to the Router

        :param path: The path for the route.
        :param handler: An asynchronous function that is used as a handler for the route.
        :param methods: A sequence of methods that the route accepts.
        """

        if not inspect.iscoroutinefunction(handler):
            raise AttributeError("Handler must be an asynchronous function")

        if path in self.paths:
            raise AttributeError(f"Path {path} already exists")

        route = Route(path, handler, methods)
        self.routes.append(route)

    def route(self, path: str, methods: Optional[Sequence[str]]) -> DCallable:
        """
        A decorator used for adding new routes to the Router

        :param path: The path for the route.
        :param methods: An asynchronous function that is used as a handler for the route.
        :return: A decorated callable function.
        """

        if path in self.paths:
            raise AttributeError(f"Path {path} already exists")

        def wrapper(handler: CoroutineFunction):
            if not inspect.iscoroutinefunction(handler):
                raise AttributeError("Handler must be an asynchronous function")

            self.register(path, handler, methods)
            return handler

        return wrapper

    async def __call__(
        self, scope: dict, receive: CoroutineFunction, send: CoroutineFunction
    ):
        if scope["type"] not in ("http", "websocket"):
            # Check whether the type of the request is HTTP or
            # websockeet, and if not, return an error
            response = JSONResponse(
                {
                    "Error": f"Invalid request type {scope['type']}, expected http or websocket"
                },
                status_code=400,
            )
            await response(scope, receive, send)
            return

        if "router" not in scope:
            scope["router"] = self

        for route in self.routes:
            match = route.path_regex.match(scope["path"])
            if match:
                if route.methods:
                    if scope["method"].lower() not in route.methods:
                        response = JSONResponse(
                            {"Error": "Method not allowed"}, status_code=405
                        )
                        await response(scope, receive, send)
                        return

                path_params = match.groupdict()
                query_params = {
                    k.decode(): v[0] for k, v in parse_qs(scope["query_string"]).items()
                }

                if route.handler.__annotations__:
                    # Only try to parse parameters if explicit types are declared
                    try:
                        query_params, path_params = parse_params(
                            query_params, path_params, route.handler.__annotations__
                        )
                    except InvalidTypeError as e:
                        # If the type conversion failed, return an error response
                        response = JSONResponse(
                            {"Error": "Bad request, failed to parse parameters"},
                            status_code=400,
                        )
                        await response(scope, receive, send)
                        return

                response = await route.handler(*path_params.values(), **query_params)
                await response(scope, receive, send)
                return

        response = JSONResponse(
            {"Error": f"URL not found {scope['path']}"}, status_code=404
        )
        await response(scope, receive, send)
