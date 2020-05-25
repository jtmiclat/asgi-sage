# asgi-sage

Security Headers Middleware for Asgi App heavily inspired by [flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman)

# Options

- [ ] feature_policy: dict = {}, force_https: bool = True,
- [x] force_https: bool = False,
- [x] force_https_permanent: bool = False,
- [x] frame_options: Optional[str] = "SAMEORIGIN",
- [x] strict_transport_security: bool = True,
- [x] strict_transport_security_preload: bool = False,
- [x] strict*transport_security_max_age: int = 60 * 60 \_ 24 \* 365,
- [ ] content_security_policy: str = "default-src: 'self'",
- [ ] content_security_policy_nonce_in: list = [],
- [ ] content_security_policy_report_only: bool = False,
- [ ] content_security_policy_report_uri: Optional[str] = None,
- [x] referrer_policy: str = "strict-origin-when-cross-origin",
- [ ] session_cookie_secure: bool = True,
- [ ] session_cookie_http_only: bool = True,
- [ ] force_file_save: bool = False,
