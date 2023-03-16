from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from user_app.router import router as user_router


app = FastAPI()

app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ConnectionsManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.client_ids: list[str] = []

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.client_ids.append(client_id)
        await self.broadcast(f"Client #{client_id} has joind the chat", client_ids=self.client_ids)


    async def disconnect(self, websocket:WebSocket, client_id:str):
        self.active_connections.remove(websocket)
        self.client_ids.remove(client_id)
        await self.broadcast(f"Client #{client_id} has left the chat", client_ids=self.client_ids)


    async def send_personal_message(self, message: str, client_ids: list[str], websocket: WebSocket):
        await websocket.send_json({"message": message, "client_ids": client_ids})

    async def broadcast(self, message:str, client_ids: list[str]):
        for connection in self.active_connections:
            await connection.send_json({"message": message, "client_ids": client_ids})

manager = ConnectionsManager()

@app.get("/users")
async def get_active_users():
    return {"users": manager.client_ids}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id:str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(message=f"you wrote {data}", client_ids=manager.client_ids, websocket=websocket)
            await manager.broadcast(message=f"client ID #{clientd_id} says: {data}", client_ids=manager.client_ids)

    except WebSocketDisconnect:
        await manager.disconnect(websocket=websocket, client_id=client_id)