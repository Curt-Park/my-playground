# Clawdbot Setup

[Clawdbot](https://docs.clawd.bot/) is a personal AI assistant that works across messaging channels (WhatsApp, Telegram, Discord, and more). The stack (`clawdbot.yaml`) deploys the gateway service with Traefik integration.

See also: [Clawdbot Docker installation](https://docs.clawd.bot/install/docker)

## Prerequisites

- Network stack deployed ([network setup](network.md))
- Create the volume directories:
  ```bash
  mkdir -p ~/docker_volumes/clawdbot/{config,workspace}
  ```

## Build and onboard

These steps are performed in the **clawdbot repository**, not in this repo.

### 1. Clone the repository

```bash
git clone https://github.com/clawdbot/clawdbot.git
cd clawdbot
```

### 2. Fix `.dockerignore`

The upstream `.dockerignore` excludes directories needed by the build. Add these negation rules to the end of `.dockerignore`:

```
!vendor/a2ui/renderers/lit
!apps/shared/ClawdbotKit/Tools/CanvasA2UI
```

### 3. Build the Docker image

```bash
docker build -t clawdbot:local -f Dockerfile .
```

> **macOS note:** If the build fails with a keychain error, unlock the keychain first:
> ```bash
> security -v unlock-keychain ~/Library/Keychains/login.keychain-db
> ```

### 4. Generate the gateway token

```bash
openssl rand -hex 32
```

Save this value — it will be used as `CLAWDBOT_GATEWAY_TOKEN`.

### 5. Run onboarding

Set the config and workspace directories to point to the volume paths used by this project, then run the onboarding wizard:

```bash
export CLAWDBOT_CONFIG_DIR=~/docker_volumes/clawdbot/config
export CLAWDBOT_WORKSPACE_DIR=~/docker_volumes/clawdbot/workspace
export CLAWDBOT_GATEWAY_TOKEN=<token from step 4>
docker compose run --rm clawdbot-cli onboard --no-install-daemon
```

When prompted during onboarding:
- Gateway bind: `lan`
- Gateway auth: `token`
- Gateway token: paste the token from step 4
- Tailscale exposure: `Off`
- Install Gateway daemon: `No`
- Enable hooks: `Yes` (accept the defaults)

The wizard also configures your AI provider credentials, which are stored in the config directory (`~/docker_volumes/clawdbot/config`).

> **Note:** The health check failure at the end of onboarding is expected — the gateway is not running during onboarding. The dashboard URLs shown are temporary and only apply to the CLI container. After deploying via Portainer, access the Control UI at `https://clawdbot.<your-domain>/`.

### 6. Set up providers (optional)

Run these commands from the clawdbot repository to add messaging channels:

**WhatsApp** (QR-based authentication):

```bash
docker compose run --rm clawdbot-cli providers login
```

**Telegram** (bot token):

```bash
docker compose run --rm clawdbot-cli providers add --provider telegram --token "<token>"
```

**Discord** (bot token):

```bash
docker compose run --rm clawdbot-cli providers add --provider discord --token "<token>"
```

See also: [Clawdbot providers documentation](https://docs.clawd.bot/providers)

### 7. Stop the local containers and remove volumes

If any containers were started during the above steps, stop them and remove the Docker volumes before deploying via Portainer. The volumes created by `docker compose` have incorrect mount paths and must be recreated by Portainer:

```bash
docker compose down
docker volume rm clawdbot_clawdbot-config clawdbot_clawdbot-workspace
```

## Environment Variables

Configure the following environment variables in Portainer when deploying:

| Variable | Description | How to get |
|---|---|---|
| `DOMAIN` | Your domain name | Same as other stacks |
| `CLAWDBOT_GATEWAY_TOKEN` | Gateway authentication token | Generated in step 4 |

The AI provider credentials (`CLAUDE_AI_SESSION_KEY`, `CLAUDE_WEB_SESSION_KEY`, `CLAUDE_WEB_COOKIE`) are optional environment variable overrides. The onboarding wizard stores credentials in the config directory, so these do not need to be set if onboarding was completed.

## Deploy

Follow the [deploy on Portainer](deploy-on-portainer.md) guide with **Compose path** set to `clawdbot.yaml`.

After deploying, the Control UI is accessible at `https://clawdbot.<your-domain>/`.

## Authentication

After setting up [Authentik](authentication.md), [register Clawdbot as an app](register-app-authentik.md).

## Volume

Clawdbot data is stored at:
- `$HOME/docker_volumes/clawdbot/config` — configuration, credentials, and session data
- `$HOME/docker_volumes/clawdbot/workspace` — workspace files
