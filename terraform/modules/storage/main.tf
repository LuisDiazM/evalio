resource "google_storage_bucket" "private_bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true

  labels = {
    owner      = "evalio"
    created_by = "terraform"
  }

  lifecycle_rule {
    condition {
      age = 90 # 3 meses (90 días)
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 180 # 6 meses (180 días)
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 365 # 12 meses (365 días)
    }
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
  }

  lifecycle_rule {
    condition {
      age = 720 # 2 años (720 días)
    }
    action {
      type = "Delete"
    }
  }
}

