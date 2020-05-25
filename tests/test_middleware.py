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


def test_strict_transport_security_true(app):
    app.add_middleware(SageMiddleware)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert "strict-transport-security" in response.headers
    response = client.get("/async-message")
    assert response.status_code == 200
    assert "strict-transport-security" in response.headers


def test_strict_transport_security_false(app):
    app.add_middleware(SageMiddleware, strict_transport_security=False)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert "strict-transport-security" not in response.headers
    response = client.get("/async-message")
    assert response.status_code == 200
    assert "strict-transport-security" not in response.headers


def test_strict_transport_security_max_age_default(app):
    app.add_middleware(SageMiddleware)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert str(60 * 60 * 24 * 365) in response.headers["strict-transport-security"]
    response = client.get("/async-message")
    assert response.status_code == 200
    assert str(60 * 60 * 24 * 365) in response.headers["strict-transport-security"]


def test_strict_transport_security_max_age_set(app):
    app.add_middleware(SageMiddleware, strict_transport_security_max_age=1000)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert str(1000) in response.headers["strict-transport-security"]
    response = client.get("/async-message")
    assert response.status_code == 200
    assert str(1000) in response.headers["strict-transport-security"]


def test_strict_transport_security_preload_default(app):
    app.add_middleware(SageMiddleware)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert "preload" not in response.headers["strict-transport-security"]
    response = client.get("/async-message")
    assert response.status_code == 200
    assert "preload" not in response.headers["strict-transport-security"]


def test_strict_transport_security_preload_true(app):
    app.add_middleware(SageMiddleware, strict_transport_security_preload=True)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert "preload" in response.headers["strict-transport-security"]
    response = client.get("/async-message")
    assert response.status_code == 200
    assert "preload" in response.headers["strict-transport-security"]


def test_referrer_policy_default(app):
    app.add_middleware(SageMiddleware)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    response = client.get("/async-message")
    assert response.status_code == 200
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"


def test_referrer_policy_origin(app):
    app.add_middleware(SageMiddleware, referrer_policy="origin")
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "SAMEORIGIN"
    response = client.get("/async-message")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "SAMEORIGIN"


def test_referrer_policy_none(app):
    app.add_middleware(SageMiddleware, referrer_policy=None)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert "Referrer-Policy" not in response.headers
    response = client.get("/async-message")
    assert response.status_code == 200
    assert "Referrer-Policy" not in response.headers


def test_force_https_true(app):
    app.add_middleware(SageMiddleware, force_https=True)
    client = TestClient(app, base_url="http://testserver")
    response = client.get("/sync-message", allow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://testserver/sync-message"

    client = TestClient(app, base_url="https://testserver")
    response = client.get("/sync-message", allow_redirects=False)
    assert response.status_code == 200

    client = TestClient(app, base_url="http://testserver")
    response = client.get("/async-message", allow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://testserver/async-message"

    client = TestClient(app, base_url="https://testserver")
    response = client.get("/async-message", allow_redirects=False)
    assert response.status_code == 200


def test_force_https_false(app):
    app.add_middleware(SageMiddleware, force_https=False)
    client = TestClient(app, base_url="http://testserver")
    response = client.get("/sync-message", allow_redirects=False)
    assert response.status_code == 200

    client = TestClient(app, base_url="https://testserver")
    response = client.get("/async-message", allow_redirects=False)
    assert response.status_code == 200


def test_force_https_permanent(app):
    app.add_middleware(SageMiddleware, force_https=True, force_https_permanent=True)
    client = TestClient(app, base_url="http://testserver")
    response = client.get("/sync-message", allow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "https://testserver/sync-message"

    client = TestClient(app, base_url="https://testserver")
    response = client.get("/sync-message", allow_redirects=False)
    assert response.status_code == 200

    client = TestClient(app, base_url="http://testserver")
    response = client.get("/async-message", allow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "https://testserver/async-message"

    client = TestClient(app, base_url="https://testserver")
    response = client.get("/async-message", allow_redirects=False)
    assert response.status_code == 200
