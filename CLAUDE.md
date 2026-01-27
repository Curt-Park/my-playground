# Project Overview

Docker-based homelab infrastructure for self-hosting services. Each service is a Docker Compose stack deployed via Portainer from a forked Git repository. All persistent data lives under `$HOME/docker_volumes/`.

## Architecture

- **Reverse proxy**: Traefik v3 with automatic HTTPS via Let's Encrypt DNS-01 challenge (Cloudflare)
- **Authentication**: Authentik SSO with forward authentication via Traefik middleware
- **DNS**: Cloudflare with automatic record management (traefik-cloudflare-companion) and DDNS
- **Deployment**: Portainer stacks from Git repository with environment variables
- **Networking**: All stacks share an external Docker network named `ingress`

## Stack Files

| File | Service | Notes |
|---|---|---|
| `init.yaml` | Portainer | Bootstrap stack, run via `make init` |
| `network.yaml` | Traefik, Cloudflare Companion, DDNS | Must be deployed first after init |
| `authentik.yaml` | Authentik SSO | PostgreSQL, Redis, server, worker |
| `n8n.yaml` | n8n workflow automation | Includes task runner |
| `monolithic.yaml` | Monolithic backend | Internal service |
| `clawdbot.yaml` | Clawdbot AI assistant | Gateway + CLI (cli profile) |

## Key Patterns

- **Volumes**: All stacks use bind mounts via named volumes with `driver_opts.device: ${HOME}/docker_volumes/<service>/...`. The `HOME` variable must be available in Portainer's environment variables.
- **Volume caching**: Docker named volumes cache `driver_opts` on first creation. If the path is wrong, you must `docker volume rm` and recreate — updating the compose file alone won't fix it.
- **Traefik labels**: Services expose themselves via Docker labels (`traefik.http.routers.*`, `traefik.http.services.*`). Authentik forward auth is applied via `authentik-proxy@docker` middleware.
- **Environment variables**: Template is in `env` (copied to `.env`). Portainer stacks use Advanced mode to paste env vars. `HOME` is not in the template but is required by all stacks for volume paths.
- **Directory creation**: Bind mount directories must exist before deploying a stack. Each doc specifies required `mkdir -p` commands.

## Makefile Commands

```
make init                              # Create ingress network + start Portainer
make down                              # Tear down init stack + remove network
make service-up STACK_NAME=<name>      # Deploy a stack via CLI
make service-down STACK_NAME=<name>    # Tear down a stack via CLI
make clawdbot-cli ARGS="<command>"     # Run clawdbot CLI command
```

## Documentation Structure

All docs are under `docs/` and linked from `README.md`:

- Setup flow: prerequisites → cloudflare → portainer → network → authentication
- Service stacks: n8n, clawdbot, monolithic (each has its own doc)
- Shared guides: `deploy-on-portainer.md` (referenced by all stacks), `register-app-authentik.md` (per-app Authentik registration)
- Optional: `docker-volumes-backup.md`

## Clawdbot Specifics

- Built from source (`docker build -t clawdbot:local`). The upstream `.dockerignore` needs negation rules for build to succeed.
- Onboarding runs via `make clawdbot-cli ARGS="onboard --no-install-daemon"` with `CLAWDBOT_CONFIG_DIR` and `CLAWDBOT_WORKSPACE_DIR` env vars pointing to volume paths.
- Gateway runs as root (`user: root` in compose) for npm global install access.
- Behind Traefik, requires `controlUi.allowInsecureAuth` and `controlUi.dangerouslyDisableDeviceAuth` in `clawdbot.json` to bypass device pairing.
- Config file: `$HOME/docker_volumes/clawdbot/config/clawdbot.json`
- After onboarding, local containers must be stopped and volumes removed before Portainer deployment (`docker compose down && docker volume rm clawdbot_clawdbot-config clawdbot_clawdbot-workspace`).

## Common Gotchas

- **`HOME` not set in Portainer**: Volume mounts fail with "path not shared from host". Add `HOME=/Users/<username>` to stack environment variables.
- **Stale Docker volumes**: Changing `driver_opts.device` in compose has no effect on existing volumes. Delete and recreate.
- **macOS Docker build**: May fail with keychain error. Fix: `security -v unlock-keychain ~/Library/Keychains/login.keychain-db`
- **macOS Bash 3.2**: No associative array support. Use `/opt/homebrew/bin/bash` or avoid scripts that need Bash 4+.
- **Clawdbot token mismatch**: The `CLAWDBOT_GATEWAY_TOKEN` env var must match `gateway.auth.token` in `clawdbot.json`. Retrieve with: `cat ~/docker_volumes/clawdbot/config/clawdbot.json | python3 -c "import sys,json; print(json.load(sys.stdin)['gateway']['auth']['token'])"`
