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
- `network.yaml`
    - traefik
    - cloudflare-companion
    - cloudflare-ddns
- `database.yaml`
    - postgresql
    - chromadb
    - vectoradmin
- `n8n.yaml`
    - n8n
- `flowise.yaml`
    - flowise
