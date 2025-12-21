output "bucket_name" {
  description = "The name of the created bucket"
  value       = google_storage_bucket.private_bucket.name
}

output "bucket_self_link" {
  description = "The self-link of the created bucket"
  value       = google_storage_bucket.private_bucket.self_link
}

output "bucket_url" {
  description = "The base URL of the bucket"
  value       = "gs://${google_storage_bucket.private_bucket.name}"
}
