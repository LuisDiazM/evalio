output "vpc_network_name" {
  description = "The name of the VPC network"
  value       = module.vpc.network_name
}

output "storage_bucket_name" {
  description = "The name of the storage bucket"
  value       = module.storage.bucket_name
}

output "database_internal_ip" {
  description = "The internal IP of the database"
  value       = module.compute_broker_db.internal_ip
}


output "forward_auth_url" {
  description = "The URL of the forward-auth service"
  value       = module.cloud_run.forward_auth_url
}

output "users_url" {
  description = "The URL of the users service"
  value       = module.cloud_run.users_url
}

output "manager_url" {
  description = "The URL of the manager service"
  value       = module.cloud_run.manager_url
}