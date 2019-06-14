import uvicorn

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import (
    JSONResponse, PlainTextResponse, RedirectResponse, StreamingResponse, 
    FileResponse)
from starlette.middleware.authentication import AuthenticationMiddleware

from starlette.templating import Jinja2Templates        # to use jinja2 template rendering

from models.user import userAuthentication
from routes import routes
import configs

# view dir
templates = Jinja2Templates(directory='templates')

app = Starlette()
app.debug = configs.DEBUG

app.mount('/static', StaticFiles(directory='statics'), name='static')


##############################
########## middlewares
##############################
# authentication
app.add_middleware(AuthenticationMiddleware, backend=userAuthentication())

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

# set cookie, its value can then be acquired by doing `request.cookies.get('test_cookie')`
@app.middleware("http")
async def set_cookie(request, call_next):
    response = await call_next(request)
    response.set_cookie('test_cookie', 42, max_age=None, expires=None, path="/", domain=None, secure=False, httponly=False)
    return response


##############################
########## rutas
##############################

# el montado de rutas se puede hacer con starlette.routing
app.mount('/', routes)


##############################
########## handlers
##############################
@app.on_event('startup')
def startup():
    print('Ready to go')
# alternativamente tambien puede usarse
# app.add_event_handler('startup', startup)


@app.on_event('shutdown')
def shutdown():
    print('turururun')


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)
    #  return RedirectResponse(url='/')


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
