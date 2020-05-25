# asgi-sage

<p align="center">
<a href="https://github.com/jtmiclat/asgi-sage/actions">
    <img src="https://github.com/jtmiclat/asgi-sage/workflows/Test%20Suite/badge.svg?branch=master" alt="Test Suite">
</a>
<a href="https://pypi.org/project/asgi-sage/">
    <img src="https://badge.fury.io/py/asgi-sage.svg" alt="Package version">
</a>
</p>

Security Headers Middleware for Asgi App heavily inspired by [flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman)

## Installation

```
pip install asgi-sage
```

## Usage

```
from asgi_sage.middleware import SageMiddleware

async def app(scope, receive, send):
    assert scope["type"] == "http"
    headers = [(b"content-type", "text/plain")]
    await send({"type": "http.response.start", "status": 200, "headers": headers})
    await send({"type": "http.response.body", "body": b"Hello, world!"})

app = SageMiddleware(app)
```

## Options

- `feature_policy: dict = {}, force_https: bool = True`
- `force_https: bool = False`
- `force_https_permanent: bool = False`
- `frame_options: Optional[str] = "SAMEORIGIN"`
- `strict_transport_security: bool = True`
- `strict_transport_security_preload: bool = False`
- `strict_transport_security_max_age: int = 60 \* 60 \_ 24 \* 365`
- `strict_transport_security_include_subdomains: bool = True`
- `content_security_policy: Optional[dict] = None`
- `referrer_policy: str = "strict-origin-when-cross-origin"`
- `session_cookie_secure: bool = True`
- `session_cookie_http_only: bool = True`

## Road Map

- [ ] Per Request overriding
- [ ] Add tests for different ASGI frameworks like [Quart](https://pgjones.gitlab.io/quart/) and [Django 3.0+](https://docs.djangoproject.com/en/3.0/topics/async/)
- [ ] Properly support websockets

- [ ] Auto Changelog

## License

MIT
