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
    - for the initial setup: https://my-host/if/flow/initial-setup/
- `filebrowser.yaml`
- `monolithic.yaml`
    - monolithic backend for supporting other services
- `n8n.yaml`
- `nocodb.yaml`
    - nocodb
    - nocodb-db (postgresql)
- `qdrant.yaml`
- `dozzle.yaml` (this requires filebrowser)

## Setting up authentication
1. go to authentik -> admin interface
2. application -> provider -> create -> select `Proxy Provider`
- name: service_name
- authorization flow: default-provider-authorization-explicit-consent (Authorize Application)
- Foward Auth
  - external host: https://service_name.my-host
3. application -> application -> create
  - name: service_name
  - slug: service_name
  - provider: service_name
4. application -> outposts -> create
  - name: FowardAuth
  - kind: Proxy
  - application: service_name or more
5. click `output deploy info` -> Copy `Authentik Token`
6. Use `Authentik Token` as `$AUTHENTIK_ACCESS_TOKEN` in `authentik.yaml`

- outpost is only created once.
- the following services use authentik auth.
  - n8n
  - filebrowser
  - n8n
    - need to set `/webhook/*` in `Unauthenticated Paths` of the n8n provider
  - nocodb
  - qdrant
  - traefik
  - [portainer - official integration](https://docs.goauthentik.io/integrations/services/portainer/)
