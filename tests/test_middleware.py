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
        response = PlainTextResponse("ok")
        response.set_cookie("key", "value")
        response.set_cookie("key2", "value2")
        return response

    @app.route("/async-message")
    async def hi2(request):
        response = PlainTextResponse("ok")
        response.set_cookie("key", "value")
        response.set_cookie("key2", "value2")
        return response

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


def test_x_frame_options_override(app):
    @app.route("/override")
    def hi(request):
        response = PlainTextResponse("ok", headers={"x-frame-options": "DENY"})
        return response

    app.add_middleware(SageMiddleware)
    client = TestClient(app)
    response = client.get("/override")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "DENY"


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


def test_strict_transport_security_include_subdomain_trur(app):
    app.add_middleware(
        SageMiddleware, strict_transport_security_include_subdomains=True
    )
    client = TestClient(app)
    response = client.get("/sync-message")
    assert "includeSubDomains" in response.headers["strict-transport-security"]
    response = client.get("/async-message")
    assert response.status_code == 200
    assert "includeSubDomains" in response.headers["strict-transport-security"]


def test_strict_transport_security_include_subdomain_false(app):
    app.add_middleware(
        SageMiddleware, strict_transport_security_include_subdomains=False
    )
    client = TestClient(app)
    response = client.get("/sync-message")
    assert "includeSubDomains" not in response.headers["strict-transport-security"]
    response = client.get("/async-message")
    assert response.status_code == 200
    assert "includeSubDomains" not in response.headers["strict-transport-security"]


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


def test_feature_policy_empty(app):
    app.add_middleware(SageMiddleware, feature_policy={})
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert "feature-policy" not in response.headers

    response = client.get("/async-message")
    assert response.status_code == 200
    assert "feature-policy" not in response.headers


def test_feature_policy_values(app):
    app.add_middleware(
        SageMiddleware, feature_policy={"geolocation": "*", "usb": "'self'"}
    )
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert "feature-policy" in response.headers
    assert "geolocation *" in response.headers["feature-policy"]
    assert "usb 'self'" in response.headers["feature-policy"]

    response = client.get("/async-message")
    assert response.status_code == 200
    assert "feature-policy" in response.headers
    assert "geolocation *" in response.headers["feature-policy"]
    assert "usb 'self'" in response.headers["feature-policy"]


def test_content_security_policy_empty(app):
    app.add_middleware(SageMiddleware, content_security_policy={})
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert "content-security-policy" not in response.headers

    response = client.get("/async-message")
    assert response.status_code == 200
    assert "content-security-policy" not in response.headers


def test_content_security_policy_values(app):
    app.add_middleware(
        SageMiddleware,
        content_security_policy={
            "default-src": "*",
            "media-src": ["media1.com", "media2.com"],
        },
    )
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert "content-security-policy" in response.headers
    assert "default-src *" in response.headers["content-security-policy"]
    assert (
        "media-src media1.com media2.com" in response.headers["content-security-policy"]
    )

    response = client.get("/async-message")
    assert response.status_code == 200
    assert "content-security-policy" in response.headers
    assert "default-src *" in response.headers["content-security-policy"]
    assert (
        "media-src media1.com media2.com" in response.headers["content-security-policy"]
    )


def test_session_cookie_secure_true(app):

    app.add_middleware(SageMiddleware, session_cookie_secure=True)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert all([v.secure for v in response.cookies]) is True


def test_session_cookie_secure_false(app):

    app.add_middleware(SageMiddleware, session_cookie_secure=False)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert all([v.secure for v in response.cookies]) is False


def test_session_cookie_http_only_true(app):

    app.add_middleware(SageMiddleware, session_cookie_http_only=True)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert all([v.has_nonstandard_attr("httponly") for v in response.cookies]) is True


def test_session_cookie_http_only_false(app):

    app.add_middleware(SageMiddleware, session_cookie_http_only=False)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert all([v.has_nonstandard_attr("httponly") for v in response.cookies]) is False


def test_content_type_nosniff_true(app):
    app.add_middleware(SageMiddleware, content_type_nosniff=True)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_content_type_nosniff_false(app):
    app.add_middleware(SageMiddleware, content_type_nosniff=False)
    client = TestClient(app)
    response = client.get("/sync-message")
    assert response.status_code == 200
    assert "X-Content-Type-Options" not in response.headers
