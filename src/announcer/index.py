import hashlib
import hmac
import json
from datetime import datetime

from announcer.utils import fmt
from debug import logger
from settings import settings
from telegram import telegram
from texts import ANNOUNCE

SUCCESS_RESPONSE = {
    "statusCode": 200,
}


def verify_signature(event):
    headers = event["headers"]

    received_signature = headers["Twitch-Eventsub-Message-Signature"]
    message = headers["Twitch-Eventsub-Message-Id"] + headers["Twitch-Eventsub-Message-Timestamp"] + event["body"]
    actual_signature = "sha256=" + hmac.new(settings.event_secret.get_secret_value().encode("utf-8"),
                                            message.encode("utf-8"), hashlib.sha256).hexdigest()

    return received_signature == actual_signature


def handle_twitch_event(body):
    if challenge := body.get("challenge"):
        return {"body": challenge}

    event = body["event"]
    username = event["broadcaster_user_name"]
    login = event["broadcaster_user_login"]
    started_at = event["started_at"]
    stream_id = event["id"]

    started_at = datetime.fromisoformat(started_at).timestamp()
    download_id = f"{login}_{stream_id}_{started_at}"

    telegram.send_message(settings.telegram.chat_id,
                          fmt(ANNOUNCE, username=username, login=login, download_id=download_id),
                          ANNOUNCE["parse_mode"])

    return SUCCESS_RESPONSE


def handle_telegram_event(body):
    message = body.get("message")
    if not message:
        return SUCCESS_RESPONSE

    if (text := message.get("text")) and text.startswith("/add"):
        username = text[5:]

        logger.info(f"Need to subscribe on {username}")

    return SUCCESS_RESPONSE


def handler(event, context):
    body = json.loads(event["body"])
    if settings.debug:
        logger.debug("Received event.", data=event)
        logger.debug("Body from received event.", data=body)

    if event["headers"].get("Twitch-Eventsub-Message-Id") and verify_signature(event):
        return handle_twitch_event(body)

    if (token := event["headers"].get(
            "X-Telegram-Bot-Api-Secret-Token")) and token == settings.event_secret.get_secret_value():
        return handle_telegram_event(body)

    if settings.debug:
        logger.debug("Event isn't from Twitch and Telegram or was faked.")

    return {
        "statusCode": 403,
    }
