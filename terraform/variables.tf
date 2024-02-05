variable "project" {
  description = "The name of the project"
}

variable "app-name" {
  description = "The name of the app"
}

variable "region" {
  description = "The region to deploy to"
}

variable "package_version" {
  description = "The sha1 git hash. Used to trigger replacement of Cloud Run on code changes."
}

variable "gcp_oauth_secret_name" {
  description = "The name of the secret on GCP containing the oauth credentials. Must already exist."
}

variable "min_instances" {
  description = "The minimum number of Cloud Run instances. Useful for reducing cold starts."
  type        = number
}

variable "deploy" {
  description = "Whether to upload the image to gcr.io"
  type        = bool
  default     = false
}

