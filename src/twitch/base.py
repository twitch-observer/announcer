import requests

from debug import logger
from settings import settings
from utils import json_or_none


class TwitchBase:
    def __init__(self):
        self.token = None

        self.get_token()

    def get_token(self):
        url = f"{settings.twitch.oauth_url}/token"

        data = {
            "grant_type": "client_credentials",
            "client_id": settings.twitch.client_id,
            "client_secret": settings.twitch.client_secret.get_secret_value(),
        }

        response = requests.post(url=url, json=data)
        response.raise_for_status()

        self.token = response.json()["access_token"]

    def _request(self, method, url, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Client-Id": settings.twitch.client_id,
        }

        kwargs["headers"] = {**kwargs.get("headers", {}), **headers}
        response = requests.request(method, url, **kwargs)

        if response.status_code == 401 and response.json()["message"] == "Invalid OAuth token":
            self.get_token()
            response = self._request(method, url, **kwargs)
            response.raise_for_status()

        if settings.debug:
            logger.debug(f"Sent request to Twitch with code {response.status_code}.", data=json_or_none(response))

        return response

    def get(self, url, params=None, **kwargs):
        return self._request("get", url, params=params, **kwargs)

    def post(self, url, json=None, data=None, **kwargs):
        return self._request("post", url, json=json, data=data, **kwargs)

    def delete(self, url, params=None, **kwargs):
        return self._request("delete", url, params=params, **kwargs)

    def get_user(self, username):
        if not username:
            return None

        url = f"{settings.twitch.api_url}/users"

        data = {
            "login": username,
        }

        response = self.get(url, data)
        response.raise_for_status()

        if not response.json()["data"]:
            logger.error(f"User with username {username} doesn't exist.")
            return None

        return response.json()["data"][0]

    def get_channel_info(self, user_id):
        url = f"{settings.twitch.api_url}/channels"

        data = {
            "broadcaster_id": user_id,
        }

        response = self.get(url, data)
        response.raise_for_status()

        return response.json()["data"][0]

    def get_users_by_ids(self, user_ids):
        url = f"{settings.twitch.api_url}/users"

        data = {
            "id": user_ids,
        }

        response = self.get(url, data)
        response.raise_for_status()

        return response.json()["data"]
