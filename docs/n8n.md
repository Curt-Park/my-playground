# n8n Setup

[n8n](https://n8n.io/) is a workflow automation platform. The stack (`n8n.yaml`) deploys the n8n server and an external task runner.

## Prerequisites

- Network stack deployed ([network setup](network.md))
- Create the volume directory:
  ```bash
  mkdir -p ~/docker_volumes/n8n/data
  ```
- Environment variables configured (see below)

## Environment Variables

Configure the following environment variables (in your `.env` file or in Portainer's environment variables):

| Variable | Description |
|---|---|
| `DOMAIN` | Your domain name — n8n is served at `https://n8n.<DOMAIN>/` |
| `EMAIL` | Used as default for `N8N_SMTP_USER` and `N8N_SMTP_SENDER` if not set |
| `TIMEZONE` | Timezone for n8n (e.g. `Asia/Seoul`, `America/New_York`) |
| `N8N_SMTP_HOST` | SMTP server hostname (e.g. `smtp.gmail.com`) |
| `N8N_SMTP_PORT` | SMTP server port (e.g. `587`) |
| `N8N_SMTP_USER` | SMTP username (defaults to `EMAIL` if not set) |
| `N8N_SMTP_PASS` | SMTP password or app password |
| `N8N_RUNNERS_AUTH_TOKEN` | Shared secret between n8n and the task runner |

Generate `N8N_RUNNERS_AUTH_TOKEN` with:

```bash
openssl rand -base64 36 | tr -d '\n'
```

## Services

### n8n

The main n8n server.

- Accessible at `n8n.your-domain`
- Protected by Authentik forward authentication
- External task runners enabled with Python support
- SMTP configured for email notifications

### n8n Task Runners

Executes workflow tasks externally, offloading work from the main n8n process.

- Connects to the n8n broker at `http://n8n:5679`
- Authenticated via `N8N_RUNNERS_AUTH_TOKEN`

## Deploy

Follow the [deploy on Portainer](deploy-on-portainer.md) guide with **Compose path** set to `n8n.yaml`.

## Authentication Note

After setting up [Authentik](authentication.md), add `/webhook/*` to **Unauthenticated Paths** in the n8n proxy provider settings. This allows external webhook triggers to bypass authentication.

## Volume

n8n data is stored at `$HOME/docker_volumes/n8n/data` and backed up via Google Drive Desktop sync.
