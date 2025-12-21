resource "google_compute_firewall" "allow_evalio_runner" {
  name    = "allow-evalio-runner-services"
  network = var.network_name

  allow {
    protocol = "tcp"
    ports    = ["22", "27017", "4222"]
  }

  source_ranges = var.allowed_sources
  target_tags   = var.target_tags
}
