terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.11.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

data "google_project" "project" {}

resource "google_project_service" "iam_credentials" {
  project                    = var.project_id
  service                    = "iamcredentials.googleapis.com"
  disable_dependent_services = true
}

module "storage" {
  source      = "./modules/storage"
  bucket_name = var.bucket_name
  region      = var.region
}

module "vpc" {
  source       = "./modules/vpc"
  network_name = "evalio-vpc"
  region       = var.region
}

module "artifact" {
  source        = "./modules/artifact"
  region        = var.region
  repository_id = "evalio-containers"
}

module "compute_broker_db" {
  source        = "./modules/compute_broker_db"
  zone          = var.zone
  region        = var.region
  db_user       = var.db_user
  db_password   = var.db_password
  subnetwork_id = module.vpc.subnet_id
}

module "firewall" {
  source          = "./modules/firewall"
  network_name    = module.vpc.network_name
  allowed_sources = var.allowed_ip_ranges
}

module "cloud_run" {
  source               = "./modules/cloud_run"
  project_id           = var.project_id
  region               = var.region
  db_user              = var.db_user
  db_password          = var.db_password
  db_internal_ip       = module.compute_broker_db.internal_ip
  vpc_connector_id     = module.vpc.connector_id
  bucket_name          = var.bucket_name
  forward_auth_version = var.forward_auth_version
  users_version        = var.users_version
  manager_version      = var.manager_version
}

