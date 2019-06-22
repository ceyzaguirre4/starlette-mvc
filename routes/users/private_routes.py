from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.responses import JSONResponse, \
    PlainTextResponse, \
    RedirectResponse, \
    StreamingResponse, \
    FileResponse, \
    HTMLResponse

from models import *

app = Starlette()

"""
All endpoints after this middleware require the connected user to be the one in the path_params.
"""
@app.middleware("http")
async def verify_user(request, call_next):
    if request.user.is_authenticated:
        if request.user.display_name == request.path_params['user_id']:
            response = await call_next(request)
            return response
    return HTMLResponse('Forbidden', status_code=403)


@app.route('/')
async def user(request):
    user_id = request.path_params['user_id']
    query = users_table.select().where(users_table.c.id == user_id)
    try:
        result = await database.fetch_one(query)
        content = {
            "name": result["name"],
        }
        return JSONResponse(content)
    except:
        return HTMLResponse(status_code=404)
