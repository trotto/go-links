resource "random_id" "db_name_suffix" {
  byte_length = 4
}

resource "google_sql_database" "this" {
  name     = "${var.project}-${var.app-name}-db"
  instance = google_sql_database_instance.this.name
}

resource "google_sql_database_instance" "this" {
  provider         = google-beta
  depends_on       = [google_service_networking_connection.private_vpc_connection]
  name             = "${var.project}-${var.app-name}-db-instance-${random_id.db_name_suffix.hex}"
  region           = "us-central1"
  database_version = "POSTGRES_13"
  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled                                  = false
      private_network                               = google_compute_network.private_network.id
      enable_private_path_for_google_cloud_services = true
    }
  }
  deletion_protection = "false"
}

resource "google_sql_user" "db_user" {
  name            = "${var.app-name}-user"
  instance        = google_sql_database_instance.this.name
  password        = random_password.password.result
  deletion_policy = "ABANDON"
}