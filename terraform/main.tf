data "docker_registry_image" "postgres" {
    name = "gerardocardenasgomez/pawtasks-db:1.0.0"
}

resource "docker_image" "postgres" {
    name = "${data.docker_registry_image.postgres.name}"
    pull_triggers = ["${data.docker_registry_image.postgres.sha256_digest}"]
}

resource "docker_network" "private_network" {
    name = "pawtasksdev"
}

resource "docker_container" "postgres" {
    name = "pawtasks_db"
    image = "${docker_image.postgres.latest}"
    restart = "unless-stopped"
    networks_advanced {
        name = "pawtasksdev"
    }

    ports {
        internal = "5432"
        ip = "10.12.0.50"
        external = "5432"
    }

    env = [
        "PAWTASKS_DB_ENV=${var.PAWTASKS_DB_ENV}",
        "PAWTASKS_DB_USER=${var.PAWTASKS_DB_USER}",
        "PAWTASKS_DB_PASSWORD=${var.PAWTASKS_DB_PASSWORD}",
        "PAWTASKS_DB_HOSTNAME=${var.PAWTASKS_DB_HOSTNAME}",
        "PAWTASKS_DB_PORT=${var.PAWTASKS_DB_PORT}",
        "PAWTASKS_SECRET_KEY=${var.PAWTASKS_SECRET_KEY}"
    ]

    provisioner "local-exec" {
        command = "sleep 5"
    }

}

resource "null_resource" "postgres_db" {
    depends_on = ["docker_container.postgres"]

    provisioner "local-exec" {
        command = "psql -U postgres -h ${docker_container.postgres.ports.0.ip} -c \"CREATE DATABASE ${var.PAWTASKS_DB_ENV}\""
    }
}

resource "null_resource" "postgres_user" {
    depends_on = ["docker_container.postgres"]

    provisioner "local-exec" {
        command = "psql -U postgres -h ${docker_container.postgres.ports.0.ip} -c \"ALTER USER ${var.PAWTASKS_DB_USER} WITH PASSWORD '${var.PAWTASKS_DB_PASSWORD}'\""
    }
}

data "docker_registry_image" "pawtasks" {
    name = "gerardocardenasgomez/pawtasks:1.0.1"
}

resource "docker_image" "pawtasks" {
    name = "${data.docker_registry_image.pawtasks.name}"
}

resource "docker_container" "pawtasks" {
    name = "pawtasks"
    image = "${docker_image.pawtasks.latest}"
    restart = "unless-stopped"
    networks_advanced {
        name = "pawtasksdev"
    }

    ports {
        internal = "8000"
        ip = "10.12.0.50"
        external = "8000"
    }

    env = [
        "PAWTASKS_DB_ENV=${var.PAWTASKS_DB_ENV}",
        "PAWTASKS_DB_USER=${var.PAWTASKS_DB_USER}",
        "PAWTASKS_DB_PASSWORD=${var.PAWTASKS_DB_PASSWORD}",
        "PAWTASKS_DB_HOSTNAME=${docker_container.postgres.ip_address}",
        "PAWTASKS_DB_PORT=${var.PAWTASKS_DB_PORT}",
        "PAWTASKS_SECRET_KEY=${var.PAWTASKS_SECRET_KEY}"
    ]

}
