# asgi-sage
Security Headers Middleware for Asgi App heavily inspired by [flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman)

# Options


- [ ] feature_policy: dict = {}, force_https: bool = True,
- [ ] force_https_permanent: bool = False,
- [X] frame_options: Optional[str] = "SAMEORIGIN",
- [ ] strict_transport_security: bool = True,
- [ ] strict_transport_security_preload: bool = False,
- [ ] strict_transport_security_max_age: int = 60 * 60 * 24 * 365,
- [ ] content_security_policy: str = "default-src: 'self'",
- [ ] content_security_policy_nonce_in: list = [],
- [ ] content_security_policy_report_only: bool = False,
- [ ] content_security_policy_report_uri: Optional[str] = None,
- [ ] legacy_content_security_policy_header: bool = True,
- [ ] referrer_policy: str = "strict-origin-when-cross-origin",
- [ ] session_cookie_secure: bool = True,
- [ ] session_cookie_http_only: bool = True,
- [ ] force_file_save: bool = False,
