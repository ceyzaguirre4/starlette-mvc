from starlette.applications import Starlette
from starlette.responses import JSONResponse, \
  PlainTextResponse, \
  RedirectResponse, \
  StreamingResponse, \
  FileResponse

app = Starlette()

@app.websocket_route('/')
async def websocket_endpoint(websocket):
    await websocket.accept()    # permite especificar protocolo con 'subprotocol='
    await websocket.send_text('Hello, websocket!')
    # await websocket.send_bytes(data)
    # await websocket.send_json(data)

    # await websocket.receive_text()
    # await websocket.receive_bytes()
    # await websocket.receive_json()

    await websocket.close()
