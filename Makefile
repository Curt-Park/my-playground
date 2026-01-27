STACK_NAME ?= network


init:
	docker network create ingress | true
	docker volume create my-self-hosting-services | true
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

show-docker:
	 docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i sh
	 # go to /var/lib/docker
