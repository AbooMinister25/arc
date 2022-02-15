import pytest
from httpx import AsyncClient

from arc import Arc
from arc.http.responses import HTTPResponse
from arc.routing import Route


def test_create_app():
    app = Arc()
    assert isinstance(app, Arc)


@pytest.mark.anyio
async def test_root():
    async def handler():
        return HTTPResponse("Hello, World")

    routes = [Route("/", handler)]
    app = Arc(routes=routes)

    async with AsyncClient(app=app, base_url="http://127.0.0.1:5000/") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert response.text == "Hello, World"


@pytest.mark.anyio
async def test_path_params():
    async def handler(bar: int):
        return HTTPResponse(f"{bar}")

    routes = [Route("/foo/{bar}", handler)]
    app = Arc(routes=routes)

    async with AsyncClient(app=app, base_url="http://127.0.0.1:5000/") as ac:
        response = await ac.get("/foo/10")

    assert response.status_code == 200
    assert response.text == "10"


@pytest.mark.anyio
async def test_query_params():
    async def handler(bar: int = None):
        return HTTPResponse(f"{bar}")

    routes = [Route("/foo", handler)]
    app = Arc(routes=routes)

    async with AsyncClient(app=app, base_url="http://127.0.0.1:5000/") as ac:
        response = await ac.get("/foo?bar=10")

    assert response.status_code == 200
    assert response.text == "10"
