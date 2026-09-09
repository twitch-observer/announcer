data "http" "twitch_observer_announcer_tg_webhook_creation" {
  url = join("", [
    "https://api.telegram.org/bot${var.tg_bot_token}/setWebhook",
    "?url=https://bot.addefan.ru:8443/${yandex_function.twitch_observer_announcer.id}",
    "&secret_token=${var.event_secret}",
  ])
}

resource "null_resource" "twitch_observer_announcer_tg_webhook_cleanup" {
  triggers = {
    bot_token = var.tg_bot_token
  }

  provisioner "local-exec" {
    when    = destroy
    command = "curl -s -X POST https://api.telegram.org/bot${self.triggers.bot_token}/deleteWebhook"
  }
}

data "http" "twitch_observer_announcer_bot_commands" {
  url    = "https://api.telegram.org/bot${var.tg_bot_token}/setMyCommands"
  method = "POST"

  request_headers = {
    Content-Type = "application/json"
  }

  request_body = jsonencode({
    commands = [
      {
        "command" : "add",
        "description" : "Добавить канал для отслеживания"
      },
      {
        "command" : "remove",
        "description" : "Удалить канал из отслеживания"
      },
      {
        "command" : "list",
        "description" : "Список отслеживаемых каналов"
      }
    ]
  })
}
