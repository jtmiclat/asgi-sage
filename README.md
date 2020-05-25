# asgi-sage

Security Headers Middleware for Asgi App heavily inspired by [flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman)

# TODO

- [x] feature_policy: dict = {}, force_https: bool = True,
- [x] force_https: bool = False,
- [x] force_https_permanent: bool = False,
- [x] frame_options: Optional[str] = "SAMEORIGIN",
- [x] strict_transport_security: bool = True,
- [x] strict_transport_security_preload: bool = False,
- [x] strict_transport_security_max_age: int = 60 \* 60 \_ 24 \* 365,
- [x] strict_transport_security_include_subdomains: bool = True,
- [x] content_security_policy: Optional[dict] = {"default-src": 'self'},
- [x] referrer_policy: str = "strict-origin-when-cross-origin",
- [x] session_cookie_secure: bool = True,
- [x] session_cookie_http_only: bool = True,
- [ ] Per View override
