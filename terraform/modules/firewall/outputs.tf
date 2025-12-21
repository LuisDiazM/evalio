output "firewall_rule_name" {
  description = "The name of the firewall rule"
  value       = google_compute_firewall.allow_evalio_runner.name
}

output "firewall_rule_id" {
  description = "The ID of the firewall rule"
  value       = google_compute_firewall.allow_evalio_runner.id
}
