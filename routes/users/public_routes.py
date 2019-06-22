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
# protected endpoint, any authorized user can access it
@requires('user_auth')
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
    # request.form() requieres python-multipart as dependency
    form = await request.form()
    username = form["name"]
    password = form["password"]
    query = users_table.select().where(users_table.c.name == username)
    try:
        results = await database.fetch_one(query)
    except:
        response = RedirectResponse('/')
    hashed_pass = results['hashed']

    valid_pass = await check_password(form["password"], hashed_pass)

    # redirect to previous path (aquired from session cookie) after login
    if 'history' in request.session and len(request.session['history']):
        previous = request.session['history'].pop()
    else:
        previous = '/'
    response = RedirectResponse(previous)
    if valid_pass:
        response.set_cookie('jwt', generate_jwt(results['id']), httponly=True)
    return response


@app.route("/", methods=["POST"])
async def new_user(request):
    # request.form() requieres python-multipart as dependency
    form = await request.form()
    password = form["password"]
    hashed_pass = await get_hashed_password(password)
    query = users_table.insert().values(
        name=form["name"],
        hashed=hashed_pass,
    )
    await database.execute(query)
    return JSONResponse({
        "name": form["name"],
    }, status_code=201)
