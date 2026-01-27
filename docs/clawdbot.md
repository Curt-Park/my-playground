# Clawdbot Setup

[Clawdbot](https://docs.clawd.bot/) is a personal AI assistant that works across messaging channels (WhatsApp, Telegram, Discord, and more). The stack (`clawdbot.yaml`) deploys the gateway service with Traefik integration.

See also: [Clawdbot Docker installation](https://docs.clawd.bot/install/docker) | [Video guide](https://youtu.be/NhJxxv3f7lI?si=Vr38L2NWy2CPhSMa)

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

> If you lost the token, you can retrieve it from the config file after onboarding:
> ```bash
> cat ~/docker_volumes/clawdbot/config/clawdbot.json | python3 -c "import sys,json; print(json.load(sys.stdin)['gateway']['auth']['token'])"
> ```

### 5. Run onboarding

Set the config and workspace directories to point to the volume paths used by this project, then run the onboarding wizard:

```bash
export CLAWDBOT_CONFIG_DIR=~/docker_volumes/clawdbot/config
export CLAWDBOT_WORKSPACE_DIR=~/docker_volumes/clawdbot/workspace
export CLAWDBOT_GATEWAY_TOKEN=<token from step 4>
make clawdbot-cli ARGS="onboard --no-install-daemon"
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

Use `make clawdbot-cli` to run CLI commands:

```bash
make clawdbot-cli ARGS="--help"            # show available commands
make clawdbot-cli ARGS="channels login"    # link WhatsApp Web (QR)
make clawdbot-cli ARGS="status"            # show channel health
make clawdbot-cli ARGS="doctor"            # health checks + quick fixes
```

See also: [Clawdbot CLI documentation](https://docs.clawd.bot/cli)

### 7. Configure Control UI for reverse proxy access

The gateway requires device pairing for non-local connections by default. Since the gateway runs behind Traefik, the Control UI will not recognize connections as local. Add the following to `~/docker_volumes/clawdbot/config/clawdbot.json` inside the `gateway` object:

```json
"controlUi": {
  "allowInsecureAuth": true,
  "dangerouslyDisableDeviceAuth": true
}
```

- `allowInsecureAuth` — allows token-only auth when the gateway sees HTTP (Traefik terminates TLS, so the gateway receives plain HTTP)
- `dangerouslyDisableDeviceAuth` — skips device pairing, allowing access with the gateway token alone

This is safe when Authentik handles authentication in front of the gateway.

### 8. Stop the local containers and remove volumes

If any containers were started during the above steps, stop them and remove the Docker volumes before deploying via Portainer. The volumes created by `docker compose` have incorrect mount paths and must be recreated by Portainer:

```bash
docker compose down
docker volume rm clawdbot_clawdbot-config clawdbot_clawdbot-workspace
```

## Environment Variables

Configure the following environment variables in Portainer when deploying:

| Variable | Description | How to get |
|---|---|---|
| `HOME` | Home directory path (e.g. `/Users/<username>`) | Required for volume mount paths — other stacks inherit this automatically, but Clawdbot requires it explicitly |
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

## Docker Limitations

- **Global npm packages are ephemeral** — packages installed with `npm i -g` (e.g. ClawdHub) are lost when the container is recreated. Re-install after redeployment.
- **No native app integration** — macOS app (system notifications), iOS/Android apps (camera/canvas) cannot connect to a containerized gateway.
- **No systemd** — the gateway daemon cannot be managed via systemd. Portainer handles container lifecycle instead.
- **Headless browser only** — no GUI inside the container, so browser-based tools (screenshots, web automation) run in headless mode only.

## Useful Knowledge

### Attaching to the container

To open a shell inside the gateway container:

```bash
docker exec -it clawdbot-gateway bash
```

Or via Portainer: **Containers** → **clawdbot-gateway** → **Console** → **Connect**.

The following sections assume you are attached to the container.

### Installing ClawdHub

[ClawdHub](https://docs.clawd.bot/tools/clawdhub) is the public skill registry for Clawdbot:

```bash
# Attach to clawdbot-gateway and run:
npm i -g clawdhub undici
```

> **Note:** Global npm packages will be lost when the container is recreated. Re-run after redeployment.

Usage:

```bash
clawdhub search "<query>"
clawdhub install <skill-slug>
clawdhub update --all
```

### Installing Homebrew

The gateway container (Debian-based) does not include Homebrew. To install it:

```bash
# Attach to clawdbot-gateway and run:
apt-get update && apt-get install -y build-essential procps curl file git
NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
source ~/.bashrc
```

After installation, `brew` is available in the current and new shell sessions.

> **Note:** Like global npm packages, this will be lost when the container is recreated.
