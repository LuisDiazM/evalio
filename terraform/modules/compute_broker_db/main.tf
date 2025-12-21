
resource "google_compute_instance" "evalio_database_messaging" {
  name         = "evalio-runner"
  machine_type = "e2-micro"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "projects/debian-cloud/global/images/debian-12-bookworm-v20250610"
      size  = 10
      type  = "pd-balanced"
    }
  }

  network_interface {
    subnetwork = var.subnetwork_id
    network_ip = google_compute_address.evalio_database_messaging_ip.address
    access_config {
      // Ephemeral public IP
    }
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    # Redirect stdout/stderr to a log file
    exec > /var/log/startup-script.log 2>&1
    set -ex

    echo "Starting startup script"

    # Install Docker and Docker Compose
    echo "Updating packages..."
    sudo apt-get update
    echo "Installing Docker..."
    sudo apt-get install -y docker.io
    echo "Starting and enabling Docker service..."
    sudo systemctl start docker
    sudo systemctl enable docker
    echo "Waiting for Docker daemon to be ready..."
    sleep 10

    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Create directories for app and volumes
    echo "Creating directories..."
    mkdir -p /opt/evalio/mongo-data
    mkdir -p /opt/evalio/nats-data

    # Change ownership for MongoDB volume
    echo "Setting permissions for Mongo data volume..."
    sudo chown -R 999:999 /opt/evalio/mongo-data

    # Create docker-compose.yaml
    echo "Creating docker-compose.yaml..."
    cat <<EOT > /opt/evalio/docker-compose.yaml
    services:
      mongo:
        image: mongo:8.0
        container_name: mongodb
        restart: always
        ports:
          - "27017:27017"
        environment:
          MONGO_INITDB_ROOT_USERNAME: ${var.db_user}
          MONGO_INITDB_ROOT_PASSWORD: ${var.db_password}
        volumes:
          - /opt/evalio/mongo-data:/data/db

      nats:
        image: nats:2.11.3
        container_name: nats
        ports:
          - "4222:4222"
          - "8222:8222"
        command: [
          "-js",
          "-m", "8222",
          "--store_dir", "/data/jetstream"
        ]
        volumes:
          - /opt/evalio/nats-data:/data/jetstream
    EOT

    # Run Docker Compose
    echo "Running Docker Compose..."
    sudo docker-compose -f /opt/evalio/docker-compose.yaml up -d

    echo "Startup script finished."
  EOF

  tags = ["evalio-runner"]
}

resource "google_compute_address" "evalio_database_messaging_ip" {
  name         = "evalio-database-messaging-ip"
  address_type = "INTERNAL"
  address      = var.internal_ip
  subnetwork   = var.subnetwork_id
  region       = var.region
}