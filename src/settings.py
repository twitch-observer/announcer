import secrets

from pydantic import SecretStr
from pydantic_settings import BaseSettings as PydanticBaseSettings


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"


class TwitchSettings(BaseSettings):
    client_id: str
    client_secret: SecretStr
    request_secret: SecretStr = secrets.token_hex(32)

    api_url: str = "https://api.twitch.tv/helix"
    eventsub_api_url: str = f"{api_url}/eventsub"
    oauth_url: str = "https://id.twitch.tv/oauth2"

    class Config:
        env_prefix = "TWITCH_"


class Settings(PydanticBaseSettings):
    twitch: TwitchSettings = TwitchSettings()


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
