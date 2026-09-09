import hashlib
import hmac

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

    def verify_signature(self, event):
        headers = event["headers"]

        received_signature = headers["Twitch-Eventsub-Message-Signature"]
        message = headers["Twitch-Eventsub-Message-Id"] + headers["Twitch-Eventsub-Message-Timestamp"] + event["body"]
        actual_signature = "sha256=" + hmac.new(settings.event_secret.get_secret_value().encode("utf-8"),
                                                message.encode("utf-8"), hashlib.sha256).hexdigest()

        return received_signature == actual_signature

    def list_tracked_streamers(self):
        subscriptions = self.list_webhooks().json()["data"]
        user_ids = {subscription["condition"]["broadcaster_user_id"] for subscription in subscriptions}
        users = self.get_users_by_ids(user_ids)
        return [user["display_name"] for user in users]


if __name__ == "__main__":
    twitch = TwitchWebhooks()

    username = "addefan"
    user_id = twitch.get_user(username)["id"]

    # response = twitch.set_stream_online_webhook(user_id, "https://functions.yandexcloud.net/d4e3e1pj20kiarv743rf")
    subscriptions = twitch.list_webhooks().json()
    from pprint import pprint
    pprint(subscriptions)

    subscriptions = subscriptions["data"]
    user_ids = [subscription["condition"]["broadcaster_user_id"] for subscription in subscriptions]
    users = twitch.get_users_by_ids(user_ids)
    id_to_name = {user["id"]: user["display_name"] for user in users}
    subscriptions = {
        subscription["id"]: id_to_name[subscription["condition"]["broadcaster_user_id"]]
        for subscription in subscriptions
    }
    print(subscriptions)

    print(twitch.list_tracked_streamers())

    # response = twitch.delete_webhook("3a8cd037-dd3f-4fa6-b296-5ff44b05dc45")
    # print(response.status_code)

    # response = twitch.set_channel_update_webhook(user_id, "https://functions.yandexcloud.net/d4e3e1pj20kiarv743rf")
    # print(response.json())
