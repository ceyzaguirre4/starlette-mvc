from starlette.applications import Starlette
from starlette.responses import JSONResponse, \
  PlainTextResponse, \
  RedirectResponse, \
  StreamingResponse, \
  FileResponse

app = Starlette()

@app.route('/')
async def users(request):
    return JSONResponse({'hello': 'users'})

@app.route('/{username}')
def user(request):
    username = request.path_params['username']
    return PlainTextResponse('Hello, %s!' % username)
