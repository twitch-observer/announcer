import requests

from settings import settings

if __name__ == "__main__":
    url = f"{settings.telegram.api_url}/setWebhook"

    data = {
        "url": settings.webhooks_callback_url,
        "secret_token": settings.event_secret.get_secret_value(),
    }

    requests.get(url, params=data)
