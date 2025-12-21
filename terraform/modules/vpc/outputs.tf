output "network_name" {
  description = "The name of the VPC network"
  value       = google_compute_network.evalio_vpc.name
}

output "network_self_link" {
  description = "The self-link of the VPC network"
  value       = google_compute_network.evalio_vpc.self_link
}

output "subnet_name" {
  description = "The name of the subnetwork"
  value       = google_compute_subnetwork.evalio_subnet_us_central.name
}

output "subnet_id" {
  description = "The ID of the subnetwork"
  value       = google_compute_subnetwork.evalio_subnet_us_central.id
}

output "connector_name" {
  description = "The name of the VPC Access Connector"
  value       = google_vpc_access_connector.connector.name
}

output "connector_id" {
  description = "The ID of the VPC Access Connector"
  value       = google_vpc_access_connector.connector.id
}
