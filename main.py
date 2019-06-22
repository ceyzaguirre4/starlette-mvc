import uvicorn
from databases import Database
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.responses import (
    JSONResponse, PlainTextResponse, RedirectResponse, StreamingResponse,
    FileResponse)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
# to use jinja2 template rendering
from starlette.templating import Jinja2Templates

from models.users import userAuthentication
from routes import routes
from models import *
import configs


app = Starlette()
app.debug = configs.DEBUG

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='statics'), name='static')


##############################
# middlewares (IMPORTANT: they are run from last to first)
##############################
# authentication
app.add_middleware(AuthenticationMiddleware, backend=userAuthentication())


@app.middleware("http")
async def update_session_history(request, call_next):
    """
    Tracks users moves through the webpage. Used in `/users/login` to redirect to last page before login.
    Because of Starlette/AsyncIO call_stack this middleware has to be above SessionMiddleware addition.
    """
    response = await call_next(request)
    history = request.session.setdefault(
        'history', []).append(request.url.path)
    return response

# for session tracking, accesible via request.session; requires `itsdangerous` module
app.add_middleware(SessionMiddleware, secret_key=configs.SECRET_KEY)

# @app.middleware("http")
# async def add_trailing_slash(request, call_next):
#     if not request.url._url.endswith('/'):
#         return RedirectResponse(request.url._url + '/')
#     response = await call_next(request)
#     return response


##############################
########## routes
##############################
app.mount('/', routes)


##############################
########## handlers
##############################
@app.on_event('startup')
async def startup():
    print('Ready to go')
    await database.connect()
# alternatively, use:
# app.add_event_handler('startup', startup)


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
    print('turururun')


@app.exception_handler(404)
async def not_found(request, exc):
    context = {"request": request}
    return templates.TemplateResponse("404.html", context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    context = {"request": request}
    return templates.TemplateResponse("500.html", context, status_code=500)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
