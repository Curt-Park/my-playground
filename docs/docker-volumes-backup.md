# Docker Volumes Backup

All Docker containers store persistent data under `$HOME/docker_volumes`. You can back up this directory by syncing it with Google Drive Desktop.

## Setup

1. Install [Google Drive Desktop](https://www.google.com/drive/download/) if not already installed
2. Open Google Drive Desktop settings
3. Add the `$HOME/docker_volumes` folder to sync
4. Select **Mirror files** or **Stream files** based on your preference
5. Wait for initial sync to complete

Once configured, your Docker volumes will automatically sync to Google Drive, providing backup and the ability to restore data across different machines.

## What gets backed up

| Service | Path |
|---|---|
| Portainer | `$HOME/docker_volumes/portainer` |
| Traefik | `$HOME/docker_volumes/traefik` (includes `acme.json` certificates) |
| Authentik | `$HOME/docker_volumes/authentik` (database, Redis, media, templates) |
| n8n | `$HOME/docker_volumes/n8n/data` |
| Clawdbot | `$HOME/docker_volumes/clawdbot` (config, workspace) |
