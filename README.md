# My Self-Hosting Services

A Docker-based homelab infrastructure for self-hosting services with centralized authentication, automated SSL certificate management, and Cloudflare integration. Services are deployed as Portainer stacks, providing a clean separation of concerns and easy management through a web UI.

The infrastructure uses Traefik as a reverse proxy with automatic HTTPS via Let's Encrypt (DNS challenge), Authentik for SSO and forward authentication, and Cloudflare for DNS management and DDoS protection.

## Main Features

**Centralized Authentication**
- **Authentik SSO**: Enterprise-grade identity provider with forward authentication
- Single sign-on across all services via Traefik middleware
- OAuth2/OIDC support for service integrations

**Network & Reverse Proxy**
- **Traefik v3**: Modern reverse proxy with automatic service discovery
- Automatic HTTPS with Let's Encrypt (DNS-01 challenge via Cloudflare)
- Wildcard SSL certificates for `*.${DOMAIN}`
- HTTP to HTTPS redirect on all services

**Cloudflare Integration**
- **traefik-cloudflare-companion**: Automatic DNS record management for Traefik services
- **cloudflare-ddns**: Dynamic DNS updates for home IP changes
- Cloudflare proxy for DDoS protection and CDN caching

**Infrastructure Management**
- **Portainer**: Web UI for managing Docker stacks and containers
- Google Drive Desktop sync for `$HOME/docker_volumes` backup
- Stack-based deployment (init, network, authentik, services)
- Environment variable configuration via `.env`

**Services**
- **n8n**: Workflow automation with task runners
- **Monolithic backend**: Supporting microservices for other applications

## Commands

```bash
make init  # then, open http://hostname:9000/
make down

STACK_NAME=$SERVICE_NAME make service-up   # requires .env
STACK_NAME=$SERVICE_NAME make service-down # requires .env
```

## Docker Volumes Backup

The `$HOME/docker_volumes` directory contains persistent data for all Docker containers. You can back up this data by syncing it with Google Drive Desktop.

**Setup Instructions:**

1. Install Google Drive Desktop app if not already installed
2. Open Google Drive Desktop settings
3. Add the `$HOME/docker_volumes` folder to sync
4. Select "Mirror files" or "Stream files" based on your preference
5. Wait for initial sync to complete

Once configured, your Docker volumes will automatically sync to Google Drive, providing backup and the ability to restore data across different machines.

## Setting up authentication

**Prerequisites:**
- Authentik service must be running (deployed via `authentik.yaml`)
- Complete initial setup at https://my-host/if/flow/initial-setup/

**Overview:**
Authentik provides forward authentication for your services through Traefik. Each protected service needs a provider (authentication config), application (represents the service), and outpost (enforces auth).

### 1. Create a Proxy Provider

*The provider defines how to authenticate and which external host to protect.*

1. Go to authentik -> admin interface
2. Application -> Provider -> Create -> Select `Proxy Provider`
3. Configure:
   - Name: `service_name`
   - Authorization flow: `default-provider-authorization-explicit-consent (Authorize Application)`
   - Forward Auth (External Host): `https://service_name.my-host`

### 2. Create an Application

*The application represents the service being protected and links to the provider.*

1. Application -> Application -> Create
2. Configure:
   - Name: `service_name`
   - Slug: `service_name`
   - Provider: `service_name` (select the provider created above)

### 3. Create/Configure Outpost

*The outpost is the forward auth middleware that enforces authentication. Create once and reuse for multiple services.*

1. Application -> Outposts -> Create (if not already created)
2. Configure:
   - Name: `ForwardAuth`
   - Type: `Proxy`
   - Applications: Select `service_name` (or multiple services)

### 4. Deploy the Outpost

1. Click the outpost -> Click `Outpost Deployment Info`
2. Copy the `Authentik Token`
3. Add token to your stack YAML as `$AUTHENTIK_ACCESS_TOKEN`

**Service-specific configurations:**
- **n8n**: Add `/webhook/*` to `Unauthenticated Paths` in the n8n provider settings
- **Traefik**: Protected by default
- **Portainer**: Use [official integration](https://docs.goauthentik.io/integrations/services/portainer/)
