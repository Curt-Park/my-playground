# n8n Setup

[n8n](https://n8n.io/) is a workflow automation platform. The stack (`n8n.yaml`) deploys the n8n server and an external task runner.

## Prerequisites

- Network stack deployed ([network setup](network.md))
- `.env` file configured with the variables below

## Environment Variables

Add these to your `.env` file:

| Variable | Description |
|---|---|
| `N8N_SMTP_HOST` | SMTP server hostname (e.g. `smtp.gmail.com`) |
| `N8N_SMTP_PORT` | SMTP server port (e.g. `587`) |
| `N8N_SMTP_USER` | SMTP username (defaults to `EMAIL` if not set) |
| `N8N_SMTP_PASS` | SMTP password or app password |
| `N8N_RUNNERS_AUTH_TOKEN` | Shared secret between n8n and the task runner (generate a random string) |

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

```bash
STACK_NAME=n8n make service-up
```

Or deploy via Portainer by uploading `n8n.yaml` as a stack with `.env` variables.

## Authentication Note

After setting up [Authentik](authentication.md), add `/webhook/*` to **Unauthenticated Paths** in the n8n proxy provider settings. This allows external webhook triggers to bypass authentication.

## Volume

n8n data is stored at `$HOME/docker_volumes/n8n/data` and backed up via Google Drive Desktop sync.
