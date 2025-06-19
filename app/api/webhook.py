import json
import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.core import security
from app.core.connection_manager import manager
from dotenv import load_dotenv

load_dotenv(".env")
SECRET = os.getenv("TWITCH_SECRET", "your_secret_key")

router = APIRouter()


async def get_msg_event_data_json(event):
    event_data = event.get("event", {})
    username = event_data.get("chatter_user_name")
    message = event_data.get("message")
    msg_obj = {
        "username": username,
        "message": message,
        "timestamp": event.get("timestamp", None)
    }
    return json.dumps(msg_obj, ensure_ascii=False)


@router.post("")
async def twitch_webhook(request: Request):
    body = await request.body()

    # Проверяем сигнатуру, чтобы всё было legit
    if not security.verify_signature(request.headers, body, SECRET):
        raise HTTPException(status_code=403, detail="Invalid signature")

    event = await request.json()
    msg_type = request.headers.get("Twitch-Eventsub-Message-Type")

    if msg_type == "webhook_callback_verification":
        # Отвечаем на challenge, чтоб Twitch пропустил
        return JSONResponse(content=event["challenge"])

    elif msg_type == "notification":
        data = await get_msg_event_data_json(event)
        print(f"[CHAT] {data}")
        await manager.broadcast(data)
        return {"status": "ok"}

    return {"status": "ignored"}
