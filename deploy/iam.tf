resource "yandex_function_iam_binding" "twitch_observer_announcer_iam" {
  function_id = yandex_function.twitch_observer_announcer.id
  role        = "functions.functionInvoker"
  members = [
    "system:allUsers",
  ]
}

resource "yandex_iam_service_account" "ymq_sa" {
  name = "twitch-observer-announcer-ymq-sa"
}

resource "yandex_iam_service_account_static_access_key" "ymq_sa_key" {
  service_account_id = yandex_iam_service_account.ymq_sa.id
}

resource "yandex_resourcemanager_folder_iam_member" "ymq_sa_role" {
  folder_id = var.folder_id
  role      = "ymq.admin"
  member    = "serviceAccount:${yandex_iam_service_account.ymq_sa.id}"
}
