from twitch.base import TwitchBase
from twitch.webhooks import TwitchWebhooks


class Twitch(TwitchBase):
    def __init__(self):
        super().__init__()
        self.webhooks = TwitchWebhooks()
