init:
	docker network create ingress | true
	docker volume create configs | true
	COMPOSE_PROJECT_NAME=init docker compose -f init.yaml up -d --remove-orphans

down:
	COMPOSE_PROJECT_NAME=init docker compose -f init.yaml down
	COMPOSE_PROJECT_NAME=init docker compose -f init.yaml rm
	docker network rm ingress
