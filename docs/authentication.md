# Setting Up Authentication

Authentik provides forward authentication for your services through Traefik. Each protected service needs a **provider** (authentication config), **application** (represents the service), and **outpost** (enforces auth).

## Prerequisites

- Authentik service must be running (deployed via `authentik.yaml`)
- Complete initial setup at `https://<your-domain>/if/flow/initial-setup/`

Before deploying, add these variables to your `.env`:

| Variable | Description |
|---|---|
| `AUTHENTIK_PG_PASS` | PostgreSQL password for Authentik database |
| `AUTHENTIK_SECRET_KEY` | Secret key for Authentik (generate a random string) |
| `AUTHENTIK_ACCESS_TOKEN` | Outpost token (obtained in step 4 below) |

## 1. Create a Proxy Provider

*The provider defines how to authenticate and which external host to protect.*

1. Go to authentik -> admin interface
2. Application -> Provider -> Create -> Select `Proxy Provider`
3. Configure:
   - Name: `service_name`
   - Authorization flow: `default-provider-authorization-explicit-consent (Authorize Application)`
   - Forward Auth (External Host): `https://service_name.<your-domain>`

## 2. Create an Application

*The application represents the service being protected and links to the provider.*

1. Application -> Application -> Create
2. Configure:
   - Name: `service_name`
   - Slug: `service_name`
   - Provider: `service_name` (select the provider created above)

## 3. Create/Configure Outpost

*The outpost is the forward auth middleware that enforces authentication. Create once and reuse for multiple services.*

1. Application -> Outposts -> Create (if not already created)
2. Configure:
   - Name: `ForwardAuth`
   - Type: `Proxy`
   - Applications: Select `service_name` (or multiple services)

## 4. Deploy the Outpost

1. Click the outpost -> Click `Outpost Deployment Info`
2. Copy the `Authentik Token`
3. Add the token to your `.env` file as `AUTHENTIK_ACCESS_TOKEN`

## Service-Specific Notes

- **n8n**: Add `/webhook/*` to `Unauthenticated Paths` in the n8n provider settings
- **Traefik**: Protected by default via `authentik-proxy@docker` middleware
- **Portainer**: Use the [official Authentik integration](https://docs.goauthentik.io/integrations/services/portainer/)
