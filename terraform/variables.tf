variable "project" {
  description = "The name of the project"
}

variable "app-name" {
  description = "The name of the app"
}

variable "region" {
  description = "The region to deploy to"
}

variable "gcp_oauth_secret_name" {
  description = "The name of the secret on GCP containing the oauth credentials. Must already exist."
}

variable "deploy" {
  description = "Whether to upload the image to gcr.io"
  type        = bool
  default     = false
}

