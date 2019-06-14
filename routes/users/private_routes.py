from starlette.applications import Starlette
from starlette.responses import JSONResponse, \
    PlainTextResponse, \
    RedirectResponse, \
    StreamingResponse, \
    FileResponse
from starlette.authentication import requires


app = Starlette()

@app.route('/me')
@requires('user_auth')    # request authentification ++ authorization level   
def user_me(request):
    username = "ceyzaguirre4"
    response = PlainTextResponse('Hello, %s!' % username)
    return response
