## Commnads
```bash
make init  # then, open http://localhost:9000/
make down
```

## Adding Stacks
1. Open portainer
2. Stack -> Add stack
3. Repository
4. Add stack inforamtion

## Basic Service Setups
- Add `network.yaml`
    - traefik
- Add `utils.yaml`
    - filebrowser
- Copy all files in `configs` into `configs` in filebrowser

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
