# Monolithic Backend Setup

The monolithic backend (`monolithic.yaml`) is a supporting microservice for other applications.

## Prerequisites

- Network stack deployed ([network setup](network.md))

## Service

- Image: `curtpark/monolithic_server:latest`
- Port: 9888 (internal, not exposed to host)
- Traefik routing is disabled by default (`traefik.enable=false`)
- Connected to the `ingress` network, so other services on the same network can reach it at `http://monolithic:9888`

## Deploy

```bash
STACK_NAME=monolithic make service-up
```

Or deploy via Portainer by uploading `monolithic.yaml` as a stack.

## Exposing via Traefik

To make the service accessible externally, update the labels in `monolithic.yaml`:

```yaml
labels:
  - traefik.enable=true
  - traefik.http.routers.monolithic.entrypoints=websecure
  - traefik.http.routers.monolithic.rule=Host(`monolithic.${DOMAIN}`)
  - traefik.http.routers.monolithic.middlewares=authentik-proxy@docker
  - traefik.http.services.monolithic.loadbalancer.server.port=9888
```
