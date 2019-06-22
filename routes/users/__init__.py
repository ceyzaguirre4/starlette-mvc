from starlette.applications import Starlette
from starlette.routing import Mount, Route, Router
from starlette.responses import JSONResponse, \
    PlainTextResponse, \
    RedirectResponse, \
    StreamingResponse, \
    FileResponse, \
    HTMLResponse

from .public_routes import app as public_routes
from .private_routes import app as private_routes

users_routes = Starlette()

users_routes.mount('/{user_id:int}', app=private_routes)
users_routes.mount('/', app=public_routes)
