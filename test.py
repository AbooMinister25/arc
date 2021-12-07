from arc import Arc
from arc.router import Route
from arc.responses import HTTPResponse


async def foo(x: int):
    return HTTPResponse(str(x))


route = Route("/foo", foo)
routes = [route]

app = Arc(routes=routes)

