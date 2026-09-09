# Twitch Observer Announcer Bot

Telegram-бот, разворачиваемый на бессерверной инфраструктуре Yandex Cloud, который следит за выбранными Twitch-каналами и отправляет анонсы о начале стримов в указанный Telegram-чат.

## Инструкция по развёртыванию

Требования:
- Иметь установленный [Terraform](https://www.terraform.io/downloads.html).
- Иметь созданное облако и каталог в [Yandex Cloud](https://console.yandex.cloud/) и их идентификаторы.
- Иметь сервисный аккаунт в [Yandex Cloud](https://console.yandex.cloud/link/iam) с ролью `admin`, путь к ключу которого указать в переменной `sa_key_file_path` на шаге 3 (по умолчанию `~/.secrets/sa-terraform.json`).
- Иметь созданного [Telegram-бота](https://t.me/botfather) и получить его токен.
- Иметь идентификатор Telegram-чата, к которому бот имеет доступ и в который он будет отправлять анонсы.
- Сгенерировать или придумать секретный ключ (состоящий из символов `A-Z`, `a-z`, `0-9`, `_` и `-` длиной от 10 до 100) для подписи и проверки достоверности сообщений от Telegram и Twitch.
- Иметь созданное [Twitch-приложение](https://dev.twitch.tv/console/apps) и получить его идентификатор и секрет.

1. Перейти в директорию для развёртывания: `cd deploy`.
2. Инициализировать, установить плагины Terraform: `terraform init`.
3. Скопировать файл с переменными: `cp terraform.tfvars.example terraform.tfvars` и заполнить его значениями.
4. Развернуть инфраструктуру в Yandex Cloud: `terraform apply`.

## Инструкция по локальному тестированию

Требования:
- Иметь установленный [Python >=3.11](https://www.python.org/downloads/).
- Иметь установленный [Poetry](https://python-poetry.org/docs/#installation).

1. Установить зависимости: `poetry install`.
2. Скопировать файл с переменными: `cp .env.example .env` и заполнить его значениями.
3. Запустить тестируемый файл: `PYTHONPATH=src poetry run python src/<path_to_file>`, например, `PYTHONPATH=src python src/twitch/webhooks.py`.
