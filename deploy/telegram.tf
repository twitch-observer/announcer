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

locals {
  bot_commands = {
    default = {
      language_code = ""
      commands = [
        {
          "command" : "add",
          "description" : "Add channel for tracking. Usage: /add <username>"
        },
        {
          "command" : "remove",
          "description" : "Delete channel from tracking. Usage: /remove <username>"
        },
        {
          "command" : "list",
          "description" : "Show list of tracked channels"
        }
      ]
    }

    ru = {
      language_code = "ru"
      commands = [
        {
          command     = "add"
          description = "Добавить канал для отслеживания. Использование: /add <никнейм>"
        },
        {
          command     = "remove"
          description = "Удалить канал из отслеживания. Использование: /remove <никнейм>"
        },
        {
          command     = "list"
          description = "Показать список отслеживаемых каналов"
        }
      ]
    }
  }
}

data "http" "twitch_observer_announcer_bot_commands" {
  for_each = local.bot_commands

  url    = "https://api.telegram.org/bot${var.tg_bot_token}/setMyCommands"
  method = "POST"

  request_headers = {
    Content-Type = "application/json"
  }

  request_body = jsonencode(each.value)
}
