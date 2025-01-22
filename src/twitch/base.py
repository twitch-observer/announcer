import requests

from debug import logger
from settings import settings


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
            return self._request(method, url, **kwargs)

        return response

    def get(self, url, params=None, **kwargs):
        return self._request("get", url, params=params, **kwargs)

    def post(self, url, json=None, data=None, **kwargs):
        return self._request("post", url, json=json, data=data, **kwargs)

    def delete(self, url, params=None, **kwargs):
        return self._request("delete", url, params=params, **kwargs)

    def get_user_id(self, username):
        url = f"{settings.twitch.api_url}/users"

        data = {
            "login": username,
        }

        response = self.get(url, data)
        response.raise_for_status()

        if not response.json()["data"]:
            logger.error(f"User with username {username} doesn't exist.")
            return None

        return response.json()["data"][0]["id"]
