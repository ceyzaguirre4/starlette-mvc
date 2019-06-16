from starlette.routing import Mount, Route, Router

from .websocket import websockets_routes
from .users import users_routes

# mounted app can also be an instance of `Router()`
routes = Router([
    # Route('/', endpoint=Homepage, methods=['GET']),
    Mount('/users', app=users_routes),
    Mount('/ws', app=websockets_routes),
])
