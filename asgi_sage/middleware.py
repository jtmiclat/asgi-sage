from typing import Optional


class SageMiddleware:
    def __init__(
        self,
        app,
        feature_policy: dict = {},
        force_https: bool = True,
        force_https_permanent: bool = False,
        frame_options: Optional[str] = "SAMEORIGIN",
        strict_transport_security: bool = True,
        strict_transport_security_preload: bool = False,
        strict_transport_security_max_age: int = 60 * 60 * 24 * 365,
        strict_transport_security_include_subdomains: bool = True,
        content_security_policy: str = "default-src: 'self'",
        content_security_policy_nonce_in: list = [],
        content_security_policy_report_only: bool = False,
        content_security_policy_report_uri: Optional[str] = None,
        referrer_policy: Optional[str] = "strict-origin-when-cross-origin",
        session_cookie_secure: bool = True,
        session_cookie_http_only: bool = True,
        force_file_save: bool = False,
    ) -> None:
        self.app = app
        self.force_https: bool = force_https
        self.force_https_permanent: bool = force_https_permanent
        self.frame_options: Optional[
            bytes
        ] = frame_options.encode() if frame_options else frame_options
        self.strict_transport_security: bool = strict_transport_security
        self.strict_transport_security_preload: bool = strict_transport_security_preload
        self.strict_transport_security_max_age: int = strict_transport_security_max_age
        self.strict_transport_security_include_subdomains: bool = strict_transport_security_include_subdomains
        self.referrer_policy: Optional[
            bytes
        ] = referrer_policy.encode() if referrer_policy else referrer_policy
        self.session_cookie_secure: bool = session_cookie_secure
        self.session_cookie_http_only: bool = session_cookie_http_only

    def _set_frame_options(self, headers: list) -> list:
        if self.frame_options:
            headers.append((b"x-frame-options", self.frame_options))
        return headers

    def _set_strict_transport_security(self, headers: list) -> list:
        if self.strict_transport_security:
            header_content = (
                b"max_age:" + str(self.strict_transport_security_max_age).encode()
            )
            if self.strict_transport_security_preload:
                header_content += b"; preload"
            if self.strict_transport_security_include_subdomains:
                header_content += b"; includeSubDomains"
            strict_transport_headers = (b"strict-transport-security", header_content)
            headers.append(strict_transport_headers)
        return headers

    def _set_referrer_policy(self, headers: list) -> list:
        if self.referrer_policy:
            headers.append((b"referrer-policy", self.referrer_policy))
        return headers

    async def redirect_to_https(self, scope, send):
        hostname = next(filter(lambda x: x[0] == b"host", scope["headers"]))[1]
        await send(
            {
                "type": "http.response.start",
                "status": 301 if self.force_https_permanent else 302,
                "headers": [
                    (b"location", b"https://" + hostname + scope["path"].encode())
                ],
            }
        )

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        if self.force_https and scope["scheme"] != "https":
            return await self.redirect_to_https(scope, send)

        def send_wrapper(response):
            headers = response.get("headers", [])
            type_ = response.get("type")
            if headers and type_ == "http.response.start":
                self._set_frame_options(headers)
                self._set_strict_transport_security(headers)
                self._set_referrer_policy(headers)
            return send(response)

        return await self.app(scope, receive, send_wrapper)
