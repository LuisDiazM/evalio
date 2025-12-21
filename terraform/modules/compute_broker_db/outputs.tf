output "instance_name" {
  description = "The name of the compute instance"
  value       = google_compute_instance.evalio_database_messaging.name
}

output "instance_self_link" {
  description = "The self-link of the compute instance"
  value       = google_compute_instance.evalio_database_messaging.self_link
}

output "internal_ip" {
  description = "The internal IP address of the compute instance"
  value       = google_compute_address.evalio_database_messaging_ip.address
}
