from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("Новый клиент подключился, бро!")

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("Клиент отключился, йоу!")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Ошибка отправки: {e}")
                await self.disconnect(connection)

manager = ConnectionManager()
