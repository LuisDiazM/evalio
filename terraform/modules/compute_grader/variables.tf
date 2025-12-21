variable "project_id" {
  description = "GCP project id"
  type        = string
}

variable "zone" {
  description = "GCP zone for the instance"
  type        = string
}

variable "db_user" {
  description = "Database username"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "bucket_name" {
  description = "GCS bucket name"
  type        = string
}

variable "subnetwork_name" {
  description = "Subnetwork name where the VM will be attached"
  type        = string
}

variable "db_internal_ip" {
  description = "Internal IP address of the database instance"
  type        = string
}

variable "docker_image" {
  description = "Container image to run on the grader VM"
  type        = string
  default     = ""
}

variable "region" {
  description = "GCP region (used to build artifact registry path)"
  type        = string
}

variable "grader_analyzer_version" {
  description = "Version tag for grader analyzer image"
  type        = string
}
