## Initial Setup
```bash
make init  # init portainer
```

Open http://localhost:9000/

## Adding Stacks
1. Open portainer
2. Stack -> Add stack
3. Repository
4. Add stack inforamtion

## Basic Service Setup
- network.yaml
    - traefik
- utils.yaml
    - filebrowser

## Additional Services
- monitor.yaml
    - dozzle
    - dcgm exporter
    - prometheus
    - grafana
- flowise.yaml
    - ollma
    - flowise
    - postgres
    - chromadb
    - vectoradmin

## References
- https://github.com/hongshibao/gpu-monitoring-docker-compose
- https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#serve_from_sub_path
