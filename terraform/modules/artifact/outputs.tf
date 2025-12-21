output "repository_name" {
  description = "The name of the Artifact Registry repository"
  value       = google_artifact_registry_repository.evalio_containers.name
}

output "repository_id" {
  description = "The ID of the Artifact Registry repository"
  value       = google_artifact_registry_repository.evalio_containers.repository_id
}
