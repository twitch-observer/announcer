import json
from datetime import datetime
from pathlib import Path

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
    user_id = event["broadcaster_user_id"]
    username = event["broadcaster_user_name"]
    login = event["broadcaster_user_login"]
    started_at = event["started_at"]
    stream_id = event["id"]

    started_at = int(datetime.fromisoformat(started_at).timestamp())
    download_id = f"{login}_{stream_id}_{started_at}"

    channel_info = twitch.get_channel_info(user_id)
    title = channel_info["title"]
    game = channel_info["game_name"]

    preview = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{login}-1920x1080.jpg"

    telegram.send_photo(settings.telegram.chat_id, preview,
                        fmt(ANNOUNCE, username=username, title=title, game=game, login=login, download_id=download_id),
                        ANNOUNCE["parse_mode"])

    return SUCCESS_RESPONSE


def handle_telegram_event(body):
    message = body.get("message")
    if not message:
        return SUCCESS_RESPONSE

    if (text := message.get("text")) and text.startswith("/add"):
        login = text[5:]

        user = twitch.get_user(login)
        if not user:
            telegram.send_message(settings.telegram.chat_id,
                                  fmt(USER_NOT_FOUND, login=login),
                                  USER_NOT_FOUND["parse_mode"])
            return SUCCESS_RESPONSE

        username = user["display_name"]
        response = twitch.webhooks.set_stream_online_webhook(user["id"], settings.webhooks_callback_url)
        if response.status_code == 202:
            telegram.send_message(settings.telegram.chat_id,
                                  fmt(USER_ADDED, username=username),
                                  USER_ADDED["parse_mode"])
            return SUCCESS_RESPONSE

        if response.status_code == 409:
            telegram.send_message(settings.telegram.chat_id,
                                  fmt(USER_ALREADY_ADDED, username=username),
                                  USER_ALREADY_ADDED["parse_mode"])
            return SUCCESS_RESPONSE

    return SUCCESS_RESPONSE


def handler(event, context):
    body = json.loads(event["body"])
    if settings.debug:
        logger.debug("Received event.", data=event)
        logger.debug("Body from received event.", data=body)

    if (message_id := event["headers"].get("Twitch-Eventsub-Message-Id")) and twitch.webhooks.verify_signature(event):
        message_id_path = Path("/tmp", message_id)
        if message_id_path.exists():
            logger.warn("Twitch sent duplicated message.")
            return SUCCESS_RESPONSE

        response = handle_twitch_event(body)
        message_id_path.touch()
        return response

    if (token := event["headers"].get("X-Telegram-Bot-Api-Secret-Token")) and token == settings.event_secret.get_secret_value():
        return handle_telegram_event(body)

    if settings.debug:
        logger.debug("Event isn't from Twitch and Telegram or was faked.")

    return {
        "statusCode": 403,
    }
