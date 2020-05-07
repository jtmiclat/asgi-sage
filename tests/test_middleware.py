import pytest
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient


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


def test_init(app):
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200