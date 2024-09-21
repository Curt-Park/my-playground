STACK_NAME ?= network


init:
	docker network create ingress | true
	COMPOSE_PROJECT_NAME=init docker compose -f init.yaml --env-file .env up -d --remove-orphans

down:
	COMPOSE_PROJECT_NAME=init docker compose -f init.yaml down
	COMPOSE_PROJECT_NAME=init docker compose -f init.yaml rm
	docker network rm ingress

service-up:
	COMPOSE_PROJECT_NAME=$(STACK_NAME) docker compose -f $(STACK_NAME).yaml --env-file .env up -d --remove-orphans

service-down:
	COMPOSE_PROJECT_NAME=$(STACK_NAME) docker compose -f $(STACK_NAME).yaml --env-file .env down
	COMPOSE_PROJECT_NAME=$(STACK_NAME) docker compose -f $(STACK_NAME).yaml --env-file .env rm
