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
- init.yaml & network.yaml
    - portainer: http://host/portainer/
    - traefik: http://host/ && http://host:8080/
- monitor.yaml (dependent on utils.yaml)
    - dozzle: http://host/dozzle/
    - grafana: http://host/grafana/
    - dcgm exporter
    - prometheus
- flowise.yaml
    - flowise: http://host/flowise/
    - vectoradmin: http://host/vectoradmin/
    - ollma
    - postgres
    - chromadb

## References
- https://github.com/hongshibao/gpu-monitoring-docker-compose
- https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#serve_from_sub_path
