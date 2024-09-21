STACK_NAME ?= network


init:
	docker network create ingress | true
	docker volume create configs | true
	docker volume create certs | true
	COMPOSE_PROJECT_NAME=init docker compose -f init.yaml --env-file .env up -d --remove-orphans
	$(MAKE) update-config
	$(MAKE) update-certs

down:
	COMPOSE_PROJECT_NAME=init docker compose -f init.yaml down
	COMPOSE_PROJECT_NAME=init docker compose -f init.yaml rm
	docker network rm ingress

service-up:
	COMPOSE_PROJECT_NAME=$(STACK_NAME) docker compose -f $(STACK_NAME).yaml --env-file .env up -d --remove-orphans

service-down:
	COMPOSE_PROJECT_NAME=$(STACK_NAME) docker compose -f $(STACK_NAME).yaml --env-file .env down
	COMPOSE_PROJECT_NAME=$(STACK_NAME) docker compose -f $(STACK_NAME).yaml --env-file .env rm

update-config:
	docker cp config/* portainer:/configs/

update-certs:
	if [ -d "certs"  ]; \
	then \
		docker cp certs/* portainer:/certs/; \
	else \
		echo "[WARN] No SSL/TLS certs in this directory"; \
	fi
