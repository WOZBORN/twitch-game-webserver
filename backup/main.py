import asyncio
import websockets
import hmac
import hashlib
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv


load_dotenv(".env")

app = Flask(__name__)

SECRET = os.getenv("TWITCH_SECRET", "your_secret_key")
connected_clients = set()


def verify_signature(req):
    twitch_signature = req.headers.get("Twitch-Eventsub-Message-Signature")
    message_id = req.headers.get("Twitch-Eventsub-Message-Id")
    timestamp = req.headers.get("Twitch-Eventsub-Message-Timestamp")
    if not all([twitch_signature, message_id, timestamp]):
        return False
    body = req.get_data()
    msg = f"{message_id}{timestamp}{body.decode()}"
    expected_hmac = "sha256=" + hmac.new(SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_hmac, twitch_signature)


@app.route("/webhook", methods=["POST"])
def twitch_webhook():
    if not verify_signature(request):
        return "Invalid signature", 403
    event = request.json
    msg_type = request.headers.get("Twitch-Eventsub-Message-Type")
    if msg_type == "webhook_callback_verification":
        return event["challenge"], 200
    elif msg_type == "notification":
        event_data = event.get("event", {})
        username = event_data.get("chatter_user_name")
        message = event_data.get("message")
        print(f"[CHAT] {username}: {message}")  # Логируем
        with open("messages.json", "a", encoding="utf-8") as f:
            f.write(f'{{"username": "{username}", "message": "{message}"}}\n')

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
