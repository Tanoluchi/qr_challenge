# Constants
SRC=qr-challenge
API_NAME = ${SRC}-server

# Commands
compose_cmd = docker-compose
down_cmd = $(compose_cmd) down --remove-orphans
attach_cmd = docker attach $(API_NAME)

down:
	@echo "Removing containers and orphans..."
	@$(down_cmd)

down_all:
	@echo "Removing containers with their volumes and images..."
	@$(down_cmd) --volumes

bash:
	docker exec -it $(API_NAME) bash

test:
	docker exec -w /code/app/test $(API_NAME) pytest -v -s

pdb:
	@$(attach_cmd)

start:
	@$(compose_cmd) start

up:
	@$(compose_cmd) up -d

build:
	@$(compose_cmd) build

logs:
	@$(compose_cmd) logs --tail=all -f