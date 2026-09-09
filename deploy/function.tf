resource "yandex_function" "twitch_observer_announcer" {
  name              = "twitch-observer-announcer"
  user_hash         = data.archive_file.twitch_observer_announcer_source.output_sha512
  runtime           = "python312"
  entrypoint        = "index.handler"
  memory            = "128"
  execution_timeout = "30"

  environment = {
    TELEGRAM_BOT_TOKEN   = var.tg_bot_token
    TWITCH_CLIENT_ID     = var.twitch_client_id
    TWITCH_CLIENT_SECRET = var.twitch_client_secret
    TELEGRAM_CHAT_ID     = var.tg_chat_id
    CLOUD_YMQ_ACCESS_KEY = yandex_iam_service_account_static_access_key.ymq_sa_key.access_key
    CLOUD_YMQ_SECRET_KEY = yandex_iam_service_account_static_access_key.ymq_sa_key.secret_key
    CLOUD_YMQ_QUEUE_URL  = yandex_message_queue.twitch_observer_announcer_queue.id
    EVENT_SECRET         = var.event_secret
    DEBUG                = var.debug
  }

  content {
    zip_filename = data.archive_file.twitch_observer_announcer_source.output_path
  }
}

resource "local_file" "requirements" {
  filename = "../src/requirements.txt"
  content  = <<-EOT
    requests
    pydantic-settings
    pydantic
    boto3
  EOT
}

data "archive_file" "twitch_observer_announcer_source" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "../build/twitch_observer_announcer_source.zip"
  excludes    = ["**/__pycache__/**"]

  depends_on = [local_file.requirements]
}

data "http" "twitch_observer_announcer_set_tg_webhook" {
  url = join("", [
    "https://api.telegram.org/bot${var.tg_bot_token}/setWebhook",
    "?url=https://bot.addefan.ru:8443/${yandex_function.twitch_observer_announcer.id}",
    "&secret_token=${var.event_secret}",
  ])
}
