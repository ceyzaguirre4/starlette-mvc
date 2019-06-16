from starlette.applications import Starlette
from starlette.responses import JSONResponse, \
    PlainTextResponse, \
    RedirectResponse, \
    StreamingResponse, \
    FileResponse
from starlette.authentication import requires

from models import *

app = Starlette()

@app.route('/me')
@requires('user_auth')    # request authentification ++ authorization level   
def user_me(request):
    username = "ceyzaguirre4"
    response = PlainTextResponse('Hello, %s!' % username)
    return response


@app.route("/", methods=["POST"])
@requires('user_auth')
async def add_user(request):
    form = await request.form()         # request.form() requieres python-multipart
    query = users_table.insert().values(
       name=form["name"],
       male=bool(form["male"])
    )
    await database.execute(query)       # await--> dont send until value has been saved
    return JSONResponse({
        "text": form["name"],
        "completed": bool(form["male"])
    })
