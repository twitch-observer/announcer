import requests

from enums import ParseMode
from utils import filter_none
from debug import logger
from settings import settings


class Telegram:
    def send_message(self, chat_id, text, parse_mode=None):
        url = f"{settings.telegram.api_url}/sendMessage"

        data = {
            "chat_id": chat_id,
            "text": text,
        }

        if parse_mode in ParseMode:
            data["parse_mode"] = parse_mode

        response = requests.post(url=url, json=data)
        if settings.debug:
            data = {"message": data, "response": response.json()}
            logger.debug(f"Sent message with code {response.status_code}.", data=data)

    def send_photo(self, chat_id, photo_url, caption=None, parse_mode=None):
        url = f"{settings.telegram.api_url}/sendPhoto"

        data = {
            "chat_id": chat_id,
            "photo": photo_url,
            **filter_none(caption=caption),
        }

        if parse_mode in ParseMode:
            data["parse_mode"] = parse_mode

        response = requests.post(url=url, json=data)
        if settings.debug:
            data = {"message": data, "response": response.json()}
            logger.debug(f"Sent photo with code {response.status_code}.", data=data)
