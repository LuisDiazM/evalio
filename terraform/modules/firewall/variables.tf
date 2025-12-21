variable "network_name" {
  description = "The name of the VPC network"
  type        = string
}

variable "allowed_sources" {
  description = "List of source IP ranges to allow"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "target_tags" {
  description = "The network tags to apply the firewall rule to"
  type        = list(string)
  default     = ["evalio-runner"]
}
