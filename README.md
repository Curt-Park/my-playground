## Commnads
```bash
make init  # then, open http://hostname:9000/
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
    - portainer: http://hostname/portainer/
    - traefik: http://hostname/ && http://hostname:8080/
- utils.yaml
    - filebrowser: http://hostname/filebrowser/
- monitor.yaml (dependent on `configs` in `filebrowser`)
    - dozzle: http://hostname/dozzle/
    - grafana: http://hostname/grafana/
    - dcgm exporter
    - prometheus
- flowise.yaml
    - flowise: http://hostname/flowise/
    - vectoradmin: http://hostname/vectoradmin/
    - ollma
    - postgres
    - chromadb
- n8n.yaml
    - n8n: http://hostname/n8n/
    - postgres

## References
- https://github.com/hongshibao/gpu-monitoring-docker-compose
- https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#serve_from_sub_path
