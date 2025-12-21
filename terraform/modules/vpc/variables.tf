variable "network_name" {
  description = "The name of the VPC network"
  type        = string
}

variable "region" {
  description = "The region for the subnetwork and connector"
  type        = string
}

variable "subnet_cidr" {
  description = "The IP CIDR range for the subnetwork"
  type        = string
  default     = "10.0.1.0/24"
}

variable "connector_cidr" {
  description = "The IP CIDR range for the VPC Access Connector"
  type        = string
  default     = "10.8.0.0/28"
}
