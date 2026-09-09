from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings as PydanticBaseSettings


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"


class TwitchSettings(BaseSettings):
    client_id: str
    client_secret: SecretStr

    api_url: str = "https://api.twitch.tv/helix"
    oauth_url: str = "https://id.twitch.tv/oauth2"

    @computed_field
    @property
    def eventsub_api_url(self) -> str:
        return f"{self.api_url}/eventsub"

    class Config:
        env_prefix = "twitch_"


class TelegramSettings(BaseSettings):
    bot_token: SecretStr
    chat_id: int

    @computed_field
    @property
    def api_url(self) -> str:
        return f"https://bot.addefan.ru:8443/tg-api/bot{self.bot_token.get_secret_value()}"

    class Config:
        env_prefix = "telegram_"

class YandexCloudSettings(BaseSettings):
    ymq_access_key: str
    ymq_secret_key: SecretStr
    ymq_queue_url: str

    class Config:
        env_prefix = "cloud_"

class Settings(BaseSettings):
    twitch: TwitchSettings = TwitchSettings()
    telegram: TelegramSettings = TelegramSettings()
    cloud: YandexCloudSettings = YandexCloudSettings()
    event_secret: SecretStr
    debug: bool = False


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
