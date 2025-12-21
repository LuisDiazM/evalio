variable "project_id" {
  description = "El ID de tu proyecto de GCP."
  type        = string
}

variable "region" {
  description = "The region to host the resources in"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "The zone to host the resources in"
  type        = string
  default     = "us-central1-b"
}

variable "db_user" {
  description = "The username for the database"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "The password for the database"
  type        = string
  sensitive   = true
}

variable "allowed_ip_ranges" {
  description = "IP ranges allowed to connect to the runner services"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "bucket_name" {
  description = "The name of the GCS bucket"
  type        = string
}

variable "forward_auth_version" {
  description = "The version of the forward-auth service"
  type        = string
  default     = "latest"
}

variable "users_version" {
  description = "The version of the users service"
  type        = string
  default     = "latest"
}

variable "manager_version" {
  description = "The version of the manager service"
  type        = string
  default     = "latest"
}
