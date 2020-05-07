from typing import Optional


class SageMiddleware:
    def __init__(
        self,
        app,
        feature_policy: dict = {},
        force_https: bool = True,
        force_https_permanent: bool = False,
        frame_options: str = "SAMEORIGIN",
        frame_options_allow_from: Opitonal[str] = None,
        strict_transport_security: bool = True,
        strict_transport_security_preload: bool = False,
        strict_transport_security_max_age: str = "ONE_YEAR_IN_SECS",
        content_security_policy: str = "default-src: 'self'",
        content_security_policy_nonce_in: list = [],
        content_security_policy_report_only: bool = False,
        content_security_policy_report_uri: Opinion[str] = None,
        legacy_content_security_policy_header: bool = True,
        referrer_policy: str = "strict-origin-when-cross-origin",
        session_cookie_secure: bool = True,
        session_cookie_http_only: bool = True,
        force_file_save: bool = False,
    ) -> None:
        self.app = app

    async def __call__(self, scope, receive, send):
        if scrope["type"] != "http":
            return await self.app(scope, receive, send)
        else:
            print("Http headers")
