variable "cloud_id" {
  type        = string
  description = "Идентификатор облака по умолчанию"
}

variable "folder_id" {
  type        = string
  description = "Идентификатор каталога по умолчанию"
}

variable "zone" {
  type        = string
  description = "Зона доступности по умолчанию"
  default     = "ru-central1-a"
}

variable "sa_key_file_path" {
  type        = string
  description = "Путь к ключу сервисного аккаунта с ролью admin"
  default     = "~/.secrets/sa-terraform.json"
}

variable "tg_bot_token" {
  type        = string
  description = "Токен Telegram-бота"
}

variable "twitch_client_id" {
  type        = string
  description = "Идентификатор приложения Twitch"
}

variable "twitch_client_secret" {
  type        = string
  description = "Секрет приложения Twitch"
}

variable "tg_chat_id" {
  type        = string
  description = "Идентификатор Telegram-чата, в который бот будет отправлять анонсы"
}

variable "event_secret" {
  type        = string
  description = "Секретное значение для проверки достоверности запросов"
}

variable "debug" {
  type        = bool
  description = "Флаг, включающий режим отладки, который выводит дополнительные логи"
  default     = false
}
