import json
from datetime import datetime

from announcer.telegram import Telegram
from announcer.texts import ANNOUNCE, USER_NOT_FOUND, USER_ADDED, USER_ALREADY_ADDED
from announcer.utils import fmt
from debug import logger
from settings import settings
from twitch import Twitch

twitch, telegram = Twitch(), Telegram()

SUCCESS_RESPONSE = {
    "statusCode": 200,
}


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

        user_id = twitch.get_user_id(username)
        if not user_id:
            telegram.send_message(settings.telegram.chat_id,
                                  fmt(USER_NOT_FOUND, username=username),
                                  USER_NOT_FOUND["parse_mode"])

        response = twitch.webhooks.set_stream_online_webhook(user_id, settings.webhooks_callback_url)
        if response.status_code == 202:
            telegram.send_message(settings.telegram.chat_id,
                                  fmt(USER_ADDED, username=username),
                                  USER_ADDED["parse_mode"])

        if response.status_code == 409:
            telegram.send_message(settings.telegram.chat_id,
                                  fmt(USER_ALREADY_ADDED, username=username),
                                  USER_ALREADY_ADDED["parse_mode"])

    return SUCCESS_RESPONSE


def handler(event, context):
    body = json.loads(event["body"])
    if settings.debug:
        logger.debug("Received event.", data=event)
        logger.debug("Body from received event.", data=body)

    if event["headers"].get("Twitch-Eventsub-Message-Id") and twitch.webhooks.verify_signature(event):
        return handle_twitch_event(body)

    if (token := event["headers"].get(
            "X-Telegram-Bot-Api-Secret-Token")) and token == settings.event_secret.get_secret_value():
        return handle_telegram_event(body)

    if settings.debug:
        logger.debug("Event isn't from Twitch and Telegram or was faked.")

    return {
        "statusCode": 403,
    }
