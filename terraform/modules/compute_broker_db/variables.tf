variable "zone" {
  description = "The zone to host the compute instance"
  type        = string
}

variable "region" {
  description = "The region to host the compute address"
  type        = string
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

variable "subnetwork_id" {
  description = "The ID of the subnetwork to attach the instance to"
  type        = string
}

variable "internal_ip" {
  description = "The internal IP address for the database"
  type        = string
  default     = "10.0.1.2"
}
