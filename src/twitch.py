import requests

from settings import settings


class Twitch:
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

        response = requests.post(url=url, data=data)
        response.raise_for_status()

        self.token = response.json()["access_token"]

    def _request(self, url, data={}, method="post"):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Client-Id": settings.twitch.client_id,
        }

        if method in {"post"}:
            response = requests.request(method, url, headers=headers, json=data)
        elif method in {"get", "delete"}:
            response = requests.request(method, url, headers=headers, params=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        if response.status_code == 401 and response.json()["message"] == "Invalid OAuth token":
            self.get_token()
            return self._request(url, data, method)

        return response

    def get_user_id(self, username):
        url = f"{settings.twitch.api_url}/users"

        data = {
            "login": username,
        }

        response = self._request(url, data, method="get")
        response.raise_for_status()

        return response.json()["data"][0]["id"]

    def set_stream_online_webhook(self, username, callback_url):
        url = f"{settings.twitch.eventsub_api_url}/subscriptions"

        data = {
            "type": "stream.online",
            "version": "1",
            "condition": {
                "broadcaster_user_id": self.get_user_id(username),
            },
            "transport": {
                "method": "webhook",
                "callback": callback_url,
                "secret": settings.twitch.request_secret.get_secret_value(),
            },
        }

        return self._request(url, data, method="post")

    def list_webhooks(self):
        url = f"{settings.twitch.eventsub_api_url}/subscriptions"

        return self._request(url, method="get")

    def delete_webhook(self, webhook_id):
        url = f"{settings.twitch.eventsub_api_url}/subscriptions"

        data = {
            "id": webhook_id,
        }

        return self._request(url, data, method="delete")

    def set_channel_update_webhook(self, username, callback_url):
        url = f"{settings.twitch.eventsub_api_url}/subscriptions"

        data = {
            "type": "channel.update",
            "version": "2",
            "condition": {
                "broadcaster_user_id": self.get_user_id(username),
            },
            "transport": {
                "method": "webhook",
                "callback": callback_url,
                "secret": settings.twitch.request_secret.get_secret_value(),
            },
        }

        return self._request(url, data, method="post")


if __name__ == "__main__":
    twitch = Twitch()

    # response = twitch.set_stream_online_webhook("addefan",
    #                                             "https://functions.yandexcloud.net/d4e3e1pj20kiarv743rf")
    # response = twitch.list_webhooks()
    # from pprint import pprint
    # pprint(response.json())

    # response = twitch.delete_webhook("5c36e5b2-fdeb-42d9-9a99-468f50285fb4")
    # print(response.status_code)

    response = twitch.set_channel_update_webhook("addefan", "https://functions.yandexcloud.net/d4e3e1pj20kiarv743rf")
    print(response.json())
