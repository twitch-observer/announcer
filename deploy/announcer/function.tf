resource "yandex_function" "twitch_observer_announcer" {
  name              = "twitch-observer-announcer"
  user_hash         = data.archive_file.twitch_observer_announcer_source.output_sha512
  runtime           = "python312"
  entrypoint        = "announcer.index.handler"
  memory            = "128"
  execution_timeout = "30"

  environment = {
    TELEGRAM_BOT_TOKEN   = var.tg_bot_token
    TWITCH_CLIENT_ID     = var.twitch_client_id
    TWITCH_CLIENT_SECRET = var.twitch_client_secret
    TELEGRAM_CHAT_ID     = var.tg_chat_id
    EVENT_SECRET         = var.event_secret
    DEBUG                = var.debug
  }

  content {
    zip_filename = data.archive_file.twitch_observer_announcer_source.output_path
  }
}

data "archive_file" "twitch_observer_announcer_source" {
  type        = "zip"
  source_dir  = "../../src"
  output_path = "../../build/twitch_observer_announcer_source.zip"
  excludes = ["**/__pycache__/**", "announcer/set_telegram_webhook.py", "downloader/**"]

  depends_on = [local_file.requirements]
}

locals {
  twitch_observer_announcer_url = "https://functions.yandexcloud.net/${yandex_function.twitch_observer_announcer.id}"
}

data "http" "twitch_observer_announcer_set_tg_webhook" {
  url = "https://api.telegram.org/bot${var.tg_bot_token}/setWebhook?url=${local.twitch_observer_announcer_url}&secret_token=${var.event_secret}"
}

resource "yandex_function_iam_binding" "exam_solver_tg_bot_iam" {
  function_id = yandex_function.twitch_observer_announcer.id
  role        = "functions.functionInvoker"
  members = [
    "system:allUsers",
  ]
}

resource "local_file" "requirements" {
  filename = "../../src/requirements.txt"
  content  = <<-EOT
    requests
    pydantic-settings
    pydantic
  EOT
}

output "twitch_observer_announcer_editor_url" {
  value       = "https://console.yandex.cloud/folders/${var.folder_id}/functions/functions/${yandex_function.twitch_observer_announcer.id}/editor"
  description = <<EOT
                Ссылка на редактор функции, в которую необходимо вручную добавить переменную окружения
                под названием WEBHOOKS_CALLBACK_URL со значением из переменной twitch_observer_announcer_url
                EOT
}

output "twitch_observer_announcer_url" {
  value       = local.twitch_observer_announcer_url
  description = "Ссылка на вызов функции, которая будет использоваться для настройки вебхуков"
}
