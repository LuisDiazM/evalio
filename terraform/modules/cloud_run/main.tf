locals {
  docker_images = {
    forward_auth = "${var.region}-docker.pkg.dev/${var.project_id}/evalio-containers/forward_auth:${var.forward_auth_version}"
    users       = "${var.region}-docker.pkg.dev/${var.project_id}/evalio-containers/users:${var.users_version}"
    manager      = "${var.region}-docker.pkg.dev/${var.project_id}/evalio-containers/manager:${var.manager_version}"
  }
}

# Secret Manager for PEM keys (loaded from files)
resource "google_secret_manager_secret" "public_pem" {
  secret_id = "evalio-public-key"
  project   = var.project_id
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "public_pem_version" {
  secret      = google_secret_manager_secret.public_pem.id
  secret_data = file("${path.module}/certs/public.pem")
}

resource "google_secret_manager_secret" "private_pem" {
  secret_id = "evalio-private-key"
  project   = var.project_id
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "private_pem_version" {
  secret      = google_secret_manager_secret.private_pem.id
  secret_data = file("${path.module}/certs/private.pem")
}

# Service Accounts for Cloud Run services
resource "google_service_account" "forward_auth_sa" {
  account_id   = "forward-auth-sa"
  display_name = "Service Account for Forward Auth Cloud Run"
  project      = var.project_id
}

resource "google_service_account" "users_sa" {
  account_id   = "users-sa"
  display_name = "Service Account for Users Cloud Run"
  project      = var.project_id
}

# Secret access permissions
resource "google_secret_manager_secret_iam_member" "forward_auth_public_key_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.public_pem.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.forward_auth_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "users_public_key_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.public_pem.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.users_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "users_private_key_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.private_pem.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.users_sa.email}"
}

###############################################################
# FORWARD-AUTH SERVICE
###############################################################
resource "google_cloud_run_v2_service" "forward_auth" {
  name                 = "forward-auth"
  location             = var.region
  deletion_protection  = false

  template {
    service_account = google_service_account.forward_auth_sa.email
    scaling {
      min_instance_count = 0
      max_instance_count = 15
    }
    
    volumes {
      name = "public-key"
      secret {
        secret = google_secret_manager_secret.public_pem.secret_id
        items {
          path    = "public.pem"
          version = "latest"
        }
      }
    }

    containers {
      image = local.docker_images.forward_auth
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      volume_mounts {
        name       = "public-key"
        mount_path = "/etc/secrets/public-key"
      }

      env {
        name  = "PUBLIC_PEM_PATH"
        value = "/etc/secrets/public-key/public.pem"
      }
    }
  }
  
  depends_on = [google_secret_manager_secret_iam_member.forward_auth_public_key_accessor]
}

resource "google_cloud_run_v2_service_iam_binding" "noauth" {
  location = google_cloud_run_v2_service.forward_auth.location
  name     = google_cloud_run_v2_service.forward_auth.name
  role     = "roles/run.invoker"
  members  = ["allUsers"]
}

###############################################################
# USERS SERVICE
###############################################################
resource "google_cloud_run_v2_service" "users" {
  name                 = "users"
  location             = var.region
  deletion_protection  = false

  template {
    service_account = google_service_account.users_sa.email
    scaling {
      min_instance_count = 0
      max_instance_count = 15
    }

    volumes {
      name = "public-key"
      secret {
        secret = google_secret_manager_secret.public_pem.secret_id
        items {
          path    = "public.pem"
          version = "latest"
        }
      }
    }

    volumes {
      name = "private-key"
      secret {
        secret = google_secret_manager_secret.private_pem.secret_id
        items {
          path    = "private.pem"
          version = "latest"
        }
      }
    }

    containers {
      image = local.docker_images.users
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
      
      volume_mounts {
        name       = "public-key"
        mount_path = "/etc/secrets/public-key"
      }

      volume_mounts {
        name       = "private-key"
        mount_path = "/etc/secrets/private-key"
      }

      env {
        name  = "MONGO_URL"
        value = "mongodb://${var.db_user}:${var.db_password}@${var.db_internal_ip}:27017/"
      }
      env {
        name  = "PUBLIC_PEM_PATH"
        value = "/etc/secrets/public-key/public.pem"
      }
      env {
        name  = "PRIVATE_PEM_PATH"
        value = "/etc/secrets/private-key/private.pem"
      }
    }
    vpc_access {
      connector = var.vpc_connector_id
      egress    = "ALL_TRAFFIC"
    }
  }

  depends_on = [
    google_secret_manager_secret_iam_member.users_public_key_accessor,
    google_secret_manager_secret_iam_member.users_private_key_accessor
  ]
}

resource "google_cloud_run_v2_service_iam_binding" "users_noauth" {
  location = google_cloud_run_v2_service.users.location
  name     = google_cloud_run_v2_service.users.name
  role     = "roles/run.invoker"
  members  = ["allUsers"]
}

###############################################################
# MANAGER SERVICE
###############################################################
resource "google_service_account" "manager_cr_sa" {
  account_id   = "manager-cr-sa"
  display_name = "Service Account for Manager Cloud Run"
  project      = var.project_id
}

# Grant permission to access GCS.
resource "google_project_iam_member" "manager_storage_access" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.manager_cr_sa.email}"
}

# Grant permission to pull images from Artifact Registry.
resource "google_project_iam_member" "manager_artifact_registry_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.manager_cr_sa.email}"
}

# Grant permission to create signed URLs.
resource "google_project_iam_member" "manager_token_creator" {
  project = var.project_id
  role    = "roles/iam.serviceAccountTokenCreator"
  member  = "serviceAccount:${google_service_account.manager_cr_sa.email}"
}

# Create a service account key
resource "google_service_account_key" "manager_cr_sa_key" {
  service_account_id = google_service_account.manager_cr_sa.name
}

# Store the key in Secret Manager
resource "google_secret_manager_secret" "manager_cr_sa_key_secret" {
  secret_id = "manager-cr-sa-key"
  project   = var.project_id

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "manager_cr_sa_key_secret_version" {
  secret      = google_secret_manager_secret.manager_cr_sa_key_secret.id
  secret_data = base64decode(google_service_account_key.manager_cr_sa_key.private_key)
}

# Allow the service account to access the secret
resource "google_secret_manager_secret_iam_member" "secret_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.manager_cr_sa_key_secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.manager_cr_sa.email}"
}

# Allow the Cloud Run Service Agent to access the secret during deployment
resource "google_secret_manager_secret_iam_member" "run_agent_secret_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.manager_cr_sa_key_secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.manager_cr_sa.email}"
}

resource "google_cloud_run_v2_service" "manager" {
  name                 = "manager"
  location             = var.region
  deletion_protection  = false

  template {
    service_account = google_service_account.manager_cr_sa.email

    scaling {
      min_instance_count = 0
      max_instance_count = 15
    }

    volumes {
      name = "gcp-key"
      secret {
        secret = google_secret_manager_secret.manager_cr_sa_key_secret.secret_id
        items {
          path    = "sa-key.json"
          version = "latest"
        }
      }
    }

    containers {
      image = local.docker_images.manager
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
      
      volume_mounts {
        name       = "gcp-key"
        mount_path = "/etc/gcp"
      }

      env {
        name  = "GOOGLE_APPLICATION_CREDENTIALS"
        value = "/etc/gcp/sa-key.json"
      }
      env {
        name  = "MONGO_URL"
        value = "mongodb://${var.db_user}:${var.db_password}@${var.db_internal_ip}:27017/"
      }
      env {
        name  = "NATS_URL"
        value = "nats://${var.db_internal_ip}:4222"
      }
      env {
        name  = "STORAGE_PROVIDER"
        value = "cloud"
      }
      env {
        name  = "GCP_BUCKET_NAME"
        value = var.bucket_name
      }
    }
    vpc_access {
      connector = var.vpc_connector_id
      egress    = "ALL_TRAFFIC"
    }
  }

  depends_on = [
    google_project_iam_member.manager_storage_access,
    google_project_iam_member.manager_artifact_registry_reader,
    google_project_iam_member.manager_token_creator,
    google_secret_manager_secret_iam_member.secret_accessor,
    google_secret_manager_secret_iam_member.run_agent_secret_accessor
  ]
}

resource "google_cloud_run_v2_service_iam_binding" "manager_noauth" {
  location = google_cloud_run_v2_service.manager.location
  name     = google_cloud_run_v2_service.manager.name
  role     = "roles/run.invoker"
  members  = ["allUsers"]
}