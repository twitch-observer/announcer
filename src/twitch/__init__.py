from twitch.base import TwitchBase
from twitch.webhooks import TwitchWebhooks


class Twitch(TwitchBase):
    def __init__(self):
        self.webhooks = TwitchWebhooks()
