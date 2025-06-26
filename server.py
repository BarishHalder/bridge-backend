# server.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
from fastapi.responses import JSONResponse

app = FastAPI()

# Dictionary to store room-wise connected clients
rooms: Dict[str, List[WebSocket]] = {}

@app.get("/")
def root():
    return JSONResponse({"message": "Bridge Chat Server is running!"})

@app.websocket("/ws/{room_id}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str):
    await websocket.accept()

    # Add client to room
    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(websocket)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            msg = f"{username}: {data}"

            # Broadcast to other clients in the same room
            for client in rooms[room_id]:
                if client != websocket:
                    await client.send_text(msg)

    except WebSocketDisconnect:
        print(f"❌ {username} disconnected from {room_id}")
        rooms[room_id].remove(websocket)