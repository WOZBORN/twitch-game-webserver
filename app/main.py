from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.api import webhook, websocket

from app.core.connection_manager import manager


app = FastAPI()

# Подключаем роутеры
app.include_router(webhook.router, prefix="/webhook", tags=["Webhook"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])

@app.get("/")
async def root():
    return {"message": "Йоу, бро! Это FastAPI сервер для Twitch и Unity"}
