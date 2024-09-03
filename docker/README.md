## Init
```bash
make init  # init the base docker stack.
make monitor  # init services for monitoring.
```

## Available Services
```bash
# base.yaml
http://hostname/portainer/
http://hostname/filebrowser/
# monitor.yaml
http://hostname/dozzle/
http://hostname/grafana/
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
