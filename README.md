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
- `n8n.yaml`
    - n8n
- `nocodb.yaml`
    - nocodb
    - nocodb-db (postgresql)
