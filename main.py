import uvicorn
from databases import Database
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.responses import (
    JSONResponse, PlainTextResponse, RedirectResponse, StreamingResponse, 
    FileResponse)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.templating import Jinja2Templates        # to use jinja2 template rendering

from models.users import userAuthentication
from routes import routes
from models import *
import configs


app = Starlette()
app.debug = configs.DEBUG

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='statics'), name='static')


##############################
########## middlewares
##############################
# authentication
app.add_middleware(AuthenticationMiddleware, backend=userAuthentication())

# app.add_middleware(SessionMiddleware, secret_key=configs.SECRET_KEY)       # for session tracking, accesible via request.session

# @app.middleware("http")
# async def add_custom_header(request, call_next):
#     """
#     always adds custom header
#     """
#     response = await call_next(request)
#     response.headers['Custom'] = 'Example'
#     return response

# @app.middleware("http")
# async def add_to_state(request, call_next):
#     """
#     uses request.state to pass information to routers
#     """
#     setattr(request.state, 'prueba', 42)
#     response = await call_next(request)
#     return response

# # set cookie, its value can then be acquired by doing `request.cookies.get('test_cookie')`
# @app.middleware("http")
# async def set_cookie(request, call_next):
#     response = await call_next(request)
#     response.set_cookie('test_cookie', 0, max_age=None, expires=None, path="/", domain=None, secure=False, httponly=False)
#     return response


##############################
########## rutas
##############################

app.mount('/', routes)


##############################
########## handlers
##############################
@app.on_event('startup')
async def startup():
    print('Ready to go')
    await database.connect()
# alternativamente tambien puede usarse
# app.add_event_handler('startup', startup)

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
    print('turururun')

@app.exception_handler(404)
async def not_found(request, exc):
    context = {"request": request}
    return templates.TemplateResponse("404.html", context, status_code=404)
    #  return RedirectResponse(url='/')

@app.exception_handler(500)
async def server_error(request, exc):
    context = {"request": request}
    return templates.TemplateResponse("500.html", context, status_code=500)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
