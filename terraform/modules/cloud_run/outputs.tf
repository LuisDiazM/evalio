output "forward_auth_url" {
  description = "The URL of the forward-auth service."
  value       = google_cloud_run_v2_service.forward_auth.uri
}

output "users_url" {
  description = "The URL of the users service."
  value       = google_cloud_run_v2_service.users.uri
}

output "manager_url" {
  description = "The URL of the manager service."
  value       = google_cloud_run_v2_service.manager.uri
}
