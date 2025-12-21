resource "google_service_account" "grader_analyzer_sa" {
  account_id   = "grader-analyzer-vm-sa"
  display_name = "Service Account for Grader Analyzer VM"
  project      = var.project_id
}

resource "google_project_iam_member" "storage_access" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.grader_analyzer_sa.email}"
}

resource "google_project_iam_member" "artifact_registry_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.grader_analyzer_sa.email}"
}

# Local values: construct docker image name from inputs if docker_image is not provided
locals {
  constructed_image = "${var.region}-docker.pkg.dev/${var.project_id}/evalio-containers/grader_analyzer:${var.grader_analyzer_version}"
  final_image       = var.docker_image != "" ? var.docker_image : local.constructed_image
}

resource "google_compute_instance" "grader_analyzer" {
  project      = var.project_id
  zone         = var.zone
  name         = "grader-analyzer"
  machine_type = "e2-micro"

  boot_disk {
    initialize_params {
      image = "projects/cos-cloud/global/images/cos-stable-121-18867-90-77"
      size  = 10
    }
  }

  network_interface {
    subnetwork = var.subnetwork_name
    access_config {}
  }

  metadata = {
    gce-container-declaration = <<-EOT
    spec:
      containers:
        - name: grader-analyzer
          image: "${local.final_image}"
          stdin: false
          tty: false
          env:
            - name: NATS_URL
              value: "nats://${var.db_internal_ip}:4222"
            - name: STORAGE_PROVIDER
              value: "gcp"
            - name: MONGO_URL
              value: "mongodb://${var.db_user}:${var.db_password}@${var.db_internal_ip}:27017/"
            - name: GCP_BUCKET_NAME
              value: "${var.bucket_name}"
      restartPolicy: Always
    EOT
  }

  service_account {
    email  = google_service_account.grader_analyzer_sa.email
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
  depends_on = [
    google_project_iam_member.storage_access,
    google_project_iam_member.artifact_registry_reader
  ]
    tags = ["evalio-runner"]

}
