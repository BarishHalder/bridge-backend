from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def ping():
    return JSONResponse({"message": "Bridge backend is running. WebSocket server ready 🚀"})

@app.websocket("/ws/{room}/{user}")
async def websocket_endpoint(websocket: WebSocket, room: str, user: str):
    await websocket.accept()
    await websocket.send_text(f"{user} joined room {room} ✅")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"{user}: {data}")
    except:
        await websocket.close()

