import asyncio
import inspect
import re
import functools
from typing import Any, Optional, Pattern, Sequence, Callable
from urllib.parse import parse_qs

from pydantic import ValidationError, parse_obj_as

from arc.http import JSONResponse
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
    """Gets the path parameters from a given path

    Uses regex to extract path parameters from a path.

    Args:
        path: A path to extract the parameters from.

    Returns:
        A list containing the path parameters

    """

    path_params = []

    for path in PATH_REGEX.finditer(path):
        param_name = path.group()[1:-1]  # The name of the path parameter
        path_params.append(param_name)

    return path_params


def compile_path_regex(path: str, path_params: list[str], method: str) -> Pattern:
    """Compiles a regex that matches the given path

    Uses the path and path parameters provided to create
    and compile a regular expression to match that path.

    Args:
        path: The path to generate the regex for.
        path_params: A list of the path parameters that the
          path contains.
        method: An optional HTTP method that the route accepts

    Returns:
        A regex pattern which matches the given path.
    """

    pattern = f"{method}_{path}"

    for param in path_params:
        pattern = pattern.replace(
            f"{{{param}}}", rf"(?P<{param}>[a-zA-Z_0-9]+)"
        )  # Replace the path parameter with a regex group for matching it

    return re.compile(pattern)


def parse_params(
    q_params: dict[str, Any],
    p_params: dict[str, Any],
    types: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Casts query and path parameters to their corresponding types.

    Args:
        q_params: A dict containing query parameters and their
          values.
        p_params: A dict containing path parameters and their
          values.
        types: A dictionary containing the types to cast the
          query and path parameters to.

    Returns:
        A tuple of two dicts which contains the parsed query
        and path parameters.

    Raises:
        ValidationError: Raises pydantic's ValidationError upon encountering an invalid value which
          cannot be parsed.
    """

    # Parses the parameters using a dictionary comprehension. `k` is the current
    # key in the original parameters dictionary, and `v` is the value to be casted.
    # The function fetches a type from `types` corresponding to the current key,
    # and if there isn't one, uses Any for casting, which effectively doesn't cast
    parsed_q = {k: parse_obj_as(types.get(k) or Any, v) for k, v in q_params.items()}
    parsed_p = {k: parse_obj_as(types.get(k) or Any, v) for k, v in p_params.items()}

    return parsed_q, parsed_p


class Route:
    """Represents a single route for an endpoint in an Arc application.

    Represents a route, contains a path, and the corresponding handler
    function for that path.

    Args:
        path: The path for the route.
        handler: A function that is used as a handler for the route.
        method: The HTTP method that the route should accept, defaults to
        `get`.

    Attributes:
        path: The path for the route.
        handler: A function that is used as a handler for the route.
        method: The HTTP method that the route should accept.
        path_params: A list of path parameters for the route.
        path_regex: A regex which matches the path for the route.
    """

    def __init__(
        self,
        path: str,
        handler: Callable,
        method: Optional[str] = "get",
    ):
        if not inspect.iscoroutinefunction(handler):
            raise AttributeError("Handler must be an asynchronous function")

        self.path = path
        self.handler = handler

        if (
            method.lower() not in METHODS
        ):  # If a given request method isn't in the global METHODS set, raise an error
            raise AttributeError(f"Invalid method {method} provide")

        self.method = method.lower()
        self.path_params: list[str] = get_path_params(
            path
        )  # Get the path parameters for the url
        self.path_regex: Pattern = compile_path_regex(
            path, self.path_params, method
        )  # Get the path regex used for matching on the URL

    def __eq__(self, other: "Route") -> bool:
        return self.path == other.path and self.method == other.method


class Router:
    """Manages and dispatches routes for an Arc application.

    Wraps an ASGI app and dispatches routes to their corresponding
    handler functions.

    Args:
        app: An ASGI application.
        routes: A sequence of routes to create the Router with.

    Attributes:
        routes: The original routes that the Router uses.
        paths: The paths for each of the routes in the Router.
        app: an ASGI application.
    """

    def __init__(
        self, app: CoroutineFunction, routes: Optional[Sequence[Route]] = None
    ):
        # self.routes: list[Route] = list(routes) if routes is not None else []
        self.routes: dict[str, Route] = (
            {route.path_regex: route for route in routes} if routes is not None else {}
        )

        self.app = app

    def register(
        self,
        path: str,
        handler: Callable,
        method: Optional[str] = None,
    ):
        """Registers a route on to the Router.

        Args:
            path: The path for the route.
            handler: A function that is used as a handler for the route.
            method: The HTTP method that the route should accept.
        """

        if not inspect.iscoroutinefunction(handler):
            raise AttributeError("Handler must be an asynchronous function")

        if f"{method}_{path}" in self.routes:
            raise AttributeError(f"Duplicate routes not allowed")

        route = Route(path, handler, method)
        self.routes[f"{method or ''}_{path}"] = route

    def route(self, path: str, method: Optional[str]) -> DCallable:
        """A decorator used for adding new routes to the Router.

        A wrapper around the Router's `register` function that is used as a
        decorator.

        Args:
            path: The path for the route.
            method: The HTTP method that the route should accept.

        Returns:
            A decorated callable function.
        """

        def wrapper(handler: Callable):
            self.register(path, handler, method)
            return handler

        return wrapper

    def register_router(self, router: "Router"):
        ...

    async def __call__(
        self, scope: dict, receive: CoroutineFunction, send: CoroutineFunction
    ):
        if scope["type"] not in ("http", "websocket"):
            # Check whether the type of the request is HTTP or
            # websocket, and if not, return an error
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

        for pattern, route in self.routes.items():
            match = route.path_regex.match(scope["path"])
            if match:
                if scope["method"].lower() != route.method:
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
                        print(query_params)
                    except ValidationError as e:
                        # If the type conversion failed, return an error response
                        response = JSONResponse(
                            {
                                "Error": f"Bad request, failed to parse parameters: {e.errors()[0]['msg']}"
                            },
                            status_code=400,
                        )
                        await response(scope, receive, send)
                        return

                try:
                    if inspect.iscoroutinefunction(route.handler):
                        response = await route.handler(
                            *path_params.values(), **query_params
                        )
                    else:
                        loop = asyncio.get_event_loop()
                        handler = functools.partial(route.handler, **query_params)

                        response = await loop.run_in_executor(
                            None, handler, *path_params.values()
                        )
                except ValidationError as e:
                    response = JSONResponse(
                        {"Error": f"Missing required query parameter {str(e)[47:-1]}"},
                        status_code=422,
                    )

                await response(scope, receive, send)
                return

        response = JSONResponse(
            {"Error": f"URL not found {scope['path']}"}, status_code=404
        )
        await response(scope, receive, send)
