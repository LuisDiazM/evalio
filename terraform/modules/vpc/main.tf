resource "google_compute_network" "evalio_vpc" {
  name                    = var.network_name
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "evalio_subnet_us_central" {
  name          = "${var.network_name}-subnet-${var.region}"
  ip_cidr_range = var.subnet_cidr
  region        = var.region
  network       = google_compute_network.evalio_vpc.name
}

resource "google_vpc_access_connector" "connector" {
  name          = "${var.network_name}-connector"
  region        = var.region
  ip_cidr_range = var.connector_cidr
  network       = google_compute_network.evalio_vpc.name
  min_instances = 2
  max_instances = 3
}