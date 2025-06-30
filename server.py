from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List

app = FastAPI()

# Allow access from any origin (you can tighten this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active connections per room
rooms: Dict[str, List[WebSocket]] = {}

@app.websocket("/ws/{room}/{user}")
async def websocket_endpoint(websocket: WebSocket, room: str, user: str):
    await websocket.accept()
    rooms.setdefault(room, []).append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            for conn in rooms[room]:
                if conn != websocket:
                    await conn.send_text(f"{user}: {data}")
    except WebSocketDisconnect:
        rooms[room].remove(websocket)
        # No need to call websocket.close(); FastAPI does it for you
