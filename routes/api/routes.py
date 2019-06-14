from starlette.applications import Starlette
from starlette.responses import JSONResponse, \
  PlainTextResponse, \
  RedirectResponse, \
  StreamingResponse, \
  FileResponse

app = Starlette()
@app.route('/')
async def api(request):
    return JSONResponse({'hello': 'api'})
