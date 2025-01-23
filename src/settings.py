from pydantic import SecretStr
from pydantic_settings import BaseSettings as PydanticBaseSettings


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"


class TwitchSettings(BaseSettings):
    client_id: str
    client_secret: SecretStr

    api_url: str = "https://api.twitch.tv/helix"
    eventsub_api_url: str = f"{api_url}/eventsub"
    oauth_url: str = "https://id.twitch.tv/oauth2"

    class Config:
        env_prefix = "twitch_"


class TelegramSettings(BaseSettings):
    bot_token: SecretStr
    chat_id: int

    api_url: str = f"https://api.telegram.org/bot{bot_token.get_secret_value()}"

    class Config:
        env_prefix = "telegram_"


class Settings(BaseSettings):
    twitch: TwitchSettings = TwitchSettings()
    telegram: TelegramSettings = TelegramSettings()
    event_secret: SecretStr
    debug: bool = False
    webhooks_callback_url: str


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
