class SageMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        headers = scope['headers']

    return await self.app(scope, receive, send)
