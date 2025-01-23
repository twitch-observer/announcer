from settings import settings
from twitch.base import TwitchBase


class TwitchWebhooks(TwitchBase):
    TWITCH_SUBSCRIPTIONS_URL = f"{settings.twitch.eventsub_api_url}/subscriptions"

    def _set_webhook(self, type_, version, condition, callback_url):
        url = self.TWITCH_SUBSCRIPTIONS_URL

        data = {
            "type": type_,
            "version": version,
            "condition": condition,
            "transport": {
                "method": "webhook",
                "callback": callback_url,
                "secret": settings.event_secret.get_secret_value(),
            },
        }

        return self.post(url, data)

    def set_stream_online_webhook(self, user_id, callback_url):
        condition = {
            "broadcaster_user_id": user_id,
        }

        return self._set_webhook("stream.online", "1", condition, callback_url)

    def list_webhooks(self):
        url = self.TWITCH_SUBSCRIPTIONS_URL

        return self.get(url)

    def delete_webhook(self, webhook_id):
        url = self.TWITCH_SUBSCRIPTIONS_URL

        data = {
            "id": webhook_id,
        }

        return self.delete(url, data)

    def set_channel_update_webhook(self, user_id, callback_url):
        condition = {
            "broadcaster_user_id": user_id,
        }

        return self._set_webhook("channel.update", "2", condition, callback_url)


if __name__ == "__main__":
    twitch = TwitchWebhooks()

    username = "addefan"
    user_id = twitch.get_user_id(username)

    # response = twitch.set_stream_online_webhook(user_id, "https://functions.yandexcloud.net/d4e3e1pj20kiarv743rf")
    response = twitch.list_webhooks()
    from pprint import pprint
    pprint(response.json())

    # response = twitch.delete_webhook("5c36e5b2-fdeb-42d9-9a99-468f50285fb4")
    # print(response.status_code)

    # response = twitch.set_channel_update_webhook(user_id, "https://functions.yandexcloud.net/d4e3e1pj20kiarv743rf")
    # print(response.json())
