variable "project_id" {
  description = "The ID of the project in which the resources will be created."
  type        = string
}

variable "region" {
  description = "The region in which the resources will be created."
  type        = string
}

variable "db_user" {
  description = "The username for the database."
  type        = string
}

variable "db_password" {
  description = "The password for the database."
  type        = string
  sensitive   = true
}

variable "db_internal_ip" {
  description = "The internal IP address of the database server."
  type        = string
}

variable "vpc_connector_id" {
  description = "The ID of the VPC Access Connector to use for the services."
  type        = string
}

variable "bucket_name" {
  description = "The name of the GCS bucket for storing data."
  type        = string
}

variable "forward_auth_version" {
  description = "The version (tag) of the forward-auth container image."
  type        = string
  default     = "latest"
}

variable "users_version" {
  description = "The version (tag) of the users container image."
  type        = string
  default     = "latest"
}

variable "manager_version" {
  description = "The version (tag) of the manager container image."
  type        = string
  default     = "latest"
}
