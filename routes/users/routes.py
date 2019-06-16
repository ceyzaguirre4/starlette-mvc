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

@app.route('/')     # methods defaults to GET
async def users(request):
    query = users_table.select()
    results = await database.fetch_all(query)
    content = [
        {
            "name": result["name"],
        }
        for result in results
    ]
    return JSONResponse(content)

@app.route("/login", methods=["POST"])
async def login_user(request):
    form = await request.form()         # request.form() requieres python-multipart as dependency
    username = form["name"]
    password = form["password"]
    query = users_table.select().where(users_table.c.name == username)
    try:
        results = await database.fetch_one(query)
    except:
        response = RedirectResponse('/')
    hashed_pass = results['hashed']

    if check_password(form["password"], hashed_pass):
        response = RedirectResponse('/')
        response.set_cookie('jwt', generate_jwt(username), httponly=True)
    else:
        response = RedirectResponse('/')
    return response

@app.route("/", methods=["POST"])
async def new_user(request):
    form = await request.form()         # request.form() requieres python-multipart as dependency
    password = form["password"]
    hashed_pass = get_hashed_password(password)
    query = users_table.insert().values(
       name=form["name"],
       hashed=hashed_pass,
    )
    await database.execute(query)
    return JSONResponse({
        "name": form["name"],
    }, status_code=201)

@app.route('/{username}')
@requires('user_auth')                  # protected endpoint, requires user to be autorized
async def user(request):
    username = request.path_params['username']
    query = users_table.select().where(users_table.c.name == username)
    try:
        result = await database.fetch_one(query)
        content = {
            "name": result["name"],
        }
        return JSONResponse(content)
    except:
        return HTMLResponse(status_code=404)
