import pytest
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from asgi_sage.middleware import SageMiddleware


@pytest.fixture
def app():
    app = Starlette()

    @app.route("/sync-message")
    def hi(request):
        return PlainTextResponse("ok")

    @app.route("/async-message")
    async def hi2(request):
        return PlainTextResponse("ok")

    return app


def test_x_frame_options_default(app):
    app.add_middleware(SageMiddleware)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "SAMEORIGIN"
    response = client.get("/async-message")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "SAMEORIGIN"


def test_x_frame_options_sameorigin(app):
    app.add_middleware(SageMiddleware, frame_options="SAMEORIGIN")
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "SAMEORIGIN"
    response = client.get("/async-message")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "SAMEORIGIN"


def test_x_frame_options_deny(app):
    app.add_middleware(SageMiddleware, frame_options="DENY")
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "DENY"
    response = client.get("/async-message")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "DENY"


def test_x_frame_options_none(app):
    app.add_middleware(SageMiddleware, frame_options=None)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert "X-Frame-Options" not in response.headers
    response = client.get("/async-message")
    assert response.status_code == 200
    assert "X-Frame-Options" not in response.headers


def test_x_frame_options_invalid(app):
    with pytest.raises(ValueError):
        app.add_middleware(SageMiddleware, frame_options="ALL")
