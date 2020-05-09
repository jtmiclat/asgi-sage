from typing import Optional

class SageMiddleware:
    def __init__(
        self,
        app,
        feature_policy: dict = {}, force_https: bool = True,
        force_https_permanent: bool = False,
        frame_options: Optional[str] = "SAMEORIGIN",
        strict_transport_security: bool = True,
        strict_transport_security_preload: bool = False,
        strict_transport_security_max_age: int = 60 * 60 * 24 * 365,
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
        self.frame_options: Optional[bytes] = frame_options.encode() if frame_options else frame_options
        self.strict_transport_security: bool  = strict_transport_security
        self.strict_transport_security_preload: bool = strict_transport_security_preload
        self.strict_transport_security_max_age: int = strict_transport_security_max_age
        self.referrer_policy: Optional[bytes]= referrer_policy.encode() if referrer_policy else referrer_policy

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        def send_wrapper(response):
            headers = response.get("headers")
            if headers:
                if self.frame_options:
                    headers.append((b"x-frame-options", self.frame_options))
                if self.strict_transport_security:
                    header_content = b"max_age:" + str(self.strict_transport_security_max_age).encode()
                    if self.strict_transport_security_preload:
                        header_content += b"; preload"
                    strict_transport_headers = (b"strict-transport-security", header_content)
                    headers.append(strict_transport_headers)

                if self.referrer_policy:
                    headers.append((b"referrer-policy", self.referrer_policy))
            return send(response)

        def receive_wrapper(request):
            return receive(request)

        return await self.app(scope, receive, send_wrapper)
