## Commnads
```bash
make init  # then, open http://hostname:9000/
make down

STACK_NAME=$SERVICE_NAME make service-up   # requires .env
STACK_NAME=$SERVICE_NAME make service-down # requires .env
```

## Adding Stacks
1. Open portainer
2. Stack -> Add stack
3. Repository
4. Add stack inforamtion
5. Deploy

## Service Stacks
- `init.yaml`
    - portainer
- `network.yaml`
    - traefik
    - cloudflare-companion
    - cloudflare-ddns
- `authentik.yaml`
    - for initial setup: https://my-host/if/flow/initial-setup/
- `filebrowser.yaml`
- `monolithic.yaml`
    - monolithic backend for supporting other services
- `n8n.yaml`
- `nocodb.yaml`
    - nocodb
    - nocodb-db (postgresql)
- `qdrant.yaml`
- `dozzle.yaml` (this requires filebrowser)
