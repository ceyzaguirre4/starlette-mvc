from starlette.applications import Starlette
from starlette.routing import Mount, Route, Router

from .public_routes import app as public_routes
from .private_routes import app as private_routes


# users_routes = Router([
#     Mount('/public', app=public_routes),
#     Mount('/private', app=private_routes)
# ])

users_routes = Starlette()

users_routes.mount('/public', public_routes)

# @users_routes.middleware("http")
# async def check_authenticated(request, call_next):
#     return await call_next(request)

users_routes.mount('/private', private_routes)
