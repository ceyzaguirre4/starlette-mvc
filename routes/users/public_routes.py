from starlette.applications import Starlette
from starlette.responses import JSONResponse, \
    PlainTextResponse, \
    RedirectResponse, \
    StreamingResponse, \
    FileResponse, \
    HTMLResponse

from models import *

app = Starlette()

@app.route('/')     # methods defaults to GET
async def users(request):
    query = users_table.select()
    results = await database.fetch_all(query)
    results = await database.fetch_all(query)
    content = [
        {
            "name": result["name"],
            "male": result["male"]
        }
        for result in results
    ]
    return JSONResponse(content)

@app.route('/{username}')
async def user(request):
    username = request.path_params['username']
    query = users_table.select().where(users_table.c.name == username)
    try:
        result = await database.fetch_one(query)
        content = {
            "name": result["name"],
            "male": result["male"]
        }
        return JSONResponse(content)
    except:
        return HTMLResponse(status_code=404)
