# Setting Up Authentication

Authentik provides forward authentication for your services through Traefik. Each protected service needs a **provider** (authentication config), **application** (represents the service), and **outpost** (enforces auth).

## Prerequisites

- Network stack deployed ([network setup](network.md))
- Create the volume directories:
  ```bash
  mkdir -p ~/docker_volumes/authentik/{database,redis,media,certs,custom_templates}
  ```
- Authentik stack deployed — follow the [deploy on Portainer](deploy-on-portainer.md) guide with **Compose path** set to `authentik.yaml`
- Complete initial setup at `https://<your-domain>/if/flow/initial-setup/`

Before deploying, configure the following environment variables (in your `.env` file or in Portainer's environment variables):

| Variable | Description |
|---|---|
| `DOMAIN` | Your domain name — Authentik is served at `https://<DOMAIN>/` |
| `AUTHENTIK_PG_PASS` | PostgreSQL password for Authentik database (max 99 characters) |
| `AUTHENTIK_SECRET_KEY` | Secret key for Authentik |

Generate `AUTHENTIK_PG_PASS` and `AUTHENTIK_SECRET_KEY` with `openssl`:

```bash
openssl rand -base64 36 | tr -d '\n'  # for AUTHENTIK_PG_PASS
openssl rand -base64 60 | tr -d '\n'  # for AUTHENTIK_SECRET_KEY
```

> **Note:** PostgreSQL limits passwords to 99 characters, so `AUTHENTIK_PG_PASS` uses a shorter output.

## Register apps

After Authentik is running, follow the [register an app with Authentik](register-app-authentik.md) guide for each service you want to protect.

### Service-Specific Notes

- **n8n**: Add `/webhook/*` to `Unauthenticated Paths` in the n8n provider settings (see [n8n setup](n8n.md))
- **Traefik**: Protected by default via `authentik-proxy@docker` middleware
- **Portainer**: Use the [official Authentik integration](https://docs.goauthentik.io/integrations/services/portainer/)
