data "google_secret_manager_secret_version_access" "basic" {
  project = var.project
  secret  = var.gcp_oauth_secret_name
}

resource "google_secret_manager_secret" "database_password" {
  secret_id = "${var.app-name}-database-password"

  replication {
    auto {}
  }
}

resource "random_password" "password" {
  length  = 16
  special = true
}

resource "google_secret_manager_secret_version" "database_password" {
  secret      = google_secret_manager_secret.database_password.id
  secret_data = random_password.password.result
}

resource "google_secret_manager_secret_iam_policy" "database_password_read_policy" {
  project     = google_secret_manager_secret.database_password.project
  secret_id   = google_secret_manager_secret.database_password.secret_id
  policy_data = data.google_iam_policy.instance_read_secret.policy_data
}