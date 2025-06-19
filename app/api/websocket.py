from typing import MutableMapping

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.connection_manager import manager

router = APIRouter()

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Если Unity шлет какие-то данные, можем их обработать тут
            text = await websocket.receive_text()
            print(f"Сообщение от Unity: {text}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
