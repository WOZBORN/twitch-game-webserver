import hmac
import hashlib

def verify_signature(headers, body: bytes, secret: str) -> bool:
    twitch_signature = headers.get("Twitch-Eventsub-Message-Signature")
    message_id = headers.get("Twitch-Eventsub-Message-Id")
    timestamp = headers.get("Twitch-Eventsub-Message-Timestamp")
    if not all([twitch_signature, message_id, timestamp]):
        return False
    msg = f"{message_id}{timestamp}{body.decode()}"
    expected_hmac = "sha256=" + hmac.new(secret.encode(), msg.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_hmac, twitch_signature)
