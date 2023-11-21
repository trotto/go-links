resource "google_service_account" "golinks" {
  account_id   = "${var.app-name}-instance-account"
  display_name = "${var.app-name} Application Service Account"
}

data "google_iam_policy" "instance_read_secret" {
  binding {
    role = "roles/secretmanager.secretAccessor"
    members = [
      "serviceAccount:${google_service_account.golinks.email}",
    ]
  }
}


resource "google_artifact_registry_repository_iam_binding" "binding" {
  project    = google_artifact_registry_repository.this.project
  location   = google_artifact_registry_repository.this.location
  repository = google_artifact_registry_repository.this.name
  role       = "roles/artifactregistry.reader"
  members    = ["serviceAccount:${google_service_account.golinks.email}"]
}