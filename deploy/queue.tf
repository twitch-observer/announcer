resource "yandex_message_queue" "twitch_observer_announcer_queue" {
  name       = "twitch-observer-announcer-queue"

  access_key = yandex_iam_service_account_static_access_key.ymq_sa_key.access_key
  secret_key = yandex_iam_service_account_static_access_key.ymq_sa_key.secret_key

  depends_on = [
    yandex_resourcemanager_folder_iam_member.ymq_sa_role
  ]
}

resource "yandex_function_trigger" "twitch_observer_announcer_queue_trigger" {
  name = "twitch-observer-announcer-queue-trigger"

  message_queue {
    batch_cutoff       = "0"
    batch_size         = "1"
    queue_id           = yandex_message_queue.twitch_observer_announcer_queue.arn
    service_account_id = yandex_iam_service_account.ymq_sa.id
  }

  function {
    id = yandex_function.twitch_observer_announcer.id
  }

  depends_on = [
    yandex_function_iam_binding.twitch_observer_announcer_iam
  ]
}
