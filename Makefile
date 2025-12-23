# Get the IDs once at the start
export UID := $(shell id -u)
export GID := $(shell id -g)

# Container variables
IMAGE_NAME := brave-voice-control
CONTAINER_NAME := scrapbot-ai


# -------------------------
# Default target
# -------------------------
.PHONY: help
help:
	@echo "Brave Music Totem - Docker Management"
	@echo "Targets:"
	@echo "  make build     Build the Docker image"
	@echo "  make up        Start the container in the background"
	@echo "  make run       Start the container in the foreground (see logs)"
	@echo "  make down      Stop and remove the container"
	@echo "  make logs      Follow container logs"
	@echo "  make shell     Open a terminal inside the running container"
	@echo "  make clean     Remove the image and cached volumes"

# -------------------------
# Docker Lifecycle
# -------------------------

.PHONY: build
build:
	docker compose build

.PHONY: up
up:
	docker compose up -d


.PHONY: run
run:
	XDG_RUNTIME_DIR=$(XDG_RUNTIME_DIR) UID=$(UID) GID=$(GID) docker compose up

.PHONY: down
down:
	docker compose down

.PHONY: logs
logs:
	docker logs -f $(CONTAINER_NAME)

.PHONY: shell
shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash

# -------------------------
# Maintenance
# -------------------------

.PHONY: clean
clean:
	docker compose down --rmi all --volumes --remove-orphans