## Init
```bash
make init  # init the base docker stack.
make monitor  # init services for monitoring.
```

## Setup (Common)
- Connect to http://hostname/portainer/
- Stacks -> Add stack
- Copy and paste the yaml files

## Flowise
- `Load variables from .env file`
  - vector-admin.env
  - chromadb.env
  - flowise.env

## References
- https://github.com/hongshibao/gpu-monitoring-docker-compose
- https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#serve_from_sub_path
