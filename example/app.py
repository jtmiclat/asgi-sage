from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from asgi_sage.middleware import SageMiddleware

app = Starlette()
app.add_middleware(
    SageMiddleware,
    feature_policy={"geolocation": "*", "usb": "'self'"},
    content_security_policy={"default-src": "'self'"},
)


@app.route("/")
async def index(request):

    response = PlainTextResponse("ok")
    response.set_cookie("key", "value")
    response.set_cookie("key2", "value2")
    return response
