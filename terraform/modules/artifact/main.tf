# Artifact Registry para imágenes Docker del monorepositorio evalio
resource "google_artifact_registry_repository" "evalio_containers" {
  location      = var.region
  repository_id = var.repository_id
  description   = "Almacenamiento de imagenes Docker del monorepositorio evalio"
  mode          = "STANDARD_REPOSITORY"
  format        = "DOCKER"


  labels = {
    owner      = "evalio"
    created_by = "terraform"
    purpose    = "docker-images"
  }

  cleanup_policies {
    id     = "keep-minimum-versions"
    action = "KEEP"
    most_recent_versions {
      package_name_prefixes = ["manager", "users", "grader_analyzer", "forward_auth"]
      keep_count            = 5
    }
  }
}
