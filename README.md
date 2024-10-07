## Commnads
```bash
make init  # then, open http://hostname:9000/
make down

COMPOSE_PROJECT_NAME=$SERVICE_NAME make serive-up   # requires .env
COMPOSE_PROJECT_NAME=$SERVICE_NAME make serive-down # requires .env
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
- `n8n.yaml`
    - n8n
- `nocodb.yaml`
    - nocodb
    - nocodb-db (postgresql)
