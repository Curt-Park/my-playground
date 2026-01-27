# Network Stack Setup

The network stack (`network.yaml`) provides reverse proxy, automatic HTTPS, and DNS management. It must be deployed before any other service stack.

## Prerequisites

- [Cloudflare setup](cloudflare.md) completed (API tokens and Zone ID configured)
- `.env` file configured with `DOMAIN`, `EMAIL`, `CF_DNS_TOKEN`, `CF_GLOBAL_TOKEN`, `DOMAIN_ZONE_ID`, and `TIMEZONE` (e.g. `America/New_York`, `America/Los_Angeles`, `Europe/London`, `Asia/Seoul`, `Asia/Tokyo`)
- Portainer running (`make init`)
- Ports 80, 443, and 8080 available on the host
- Create the volume directory:
  ```bash
  mkdir -p ~/docker_volumes/traefik
  ```

## Services

### Traefik

Reverse proxy with automatic service discovery and HTTPS.

- Listens on ports 80 (HTTP), 443 (HTTPS), and 8080 (dashboard)
- HTTP requests are automatically redirected to HTTPS
- Obtains a wildcard certificate (`*.your-domain`) from Let's Encrypt via DNS-01 challenge through Cloudflare
- Trusts Cloudflare IP ranges for `X-Forwarded-*` headers
- Dashboard accessible at `traefik.your-domain` (protected by Authentik after [authentication setup](authentication.md))

### Cloudflare Companion

Watches Docker containers for Traefik labels and automatically creates CNAME DNS records in Cloudflare.

- When a new service with `traefik.http.routers.*.rule=Host(...)` labels starts, a proxied CNAME record is created automatically
- No manual DNS record creation needed for new services

### Cloudflare DDNS

Updates the root domain's A record to the host's current public IP.

- Keeps your homelab accessible when your ISP changes your IP address
- Runs with a read-only filesystem and dropped capabilities for security

## Deploy

Follow the [deploy on Portainer](deploy-on-portainer.md) guide with **Compose path** set to `network.yaml`.

## Verify

1. Check that Traefik is running: open `http://<hostname>:8080` for the dashboard
2. Confirm the wildcard certificate was issued: check the Traefik dashboard under **HTTPS** -> **Certificates**
3. DNS records in Cloudflare are automatically created and updated — Cloudflare Companion creates CNAME records for new services, and Cloudflare DDNS keeps the root domain's A record pointing to your current public IP. No manual DNS configuration is needed after deploying this stack.
4. `https://portainer.<your-domain>/` will be available after this step

## Volume

Traefik stores its ACME certificate data at `$HOME/docker_volumes/traefik/acme.json`. This is persisted across restarts and backed up via Google Drive Desktop sync.
