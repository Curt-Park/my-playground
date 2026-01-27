# Portainer Setup

## 1. Set up environment variables

Copy the `env` template to `.env` and fill in the values:

```bash
cp env .env
```

At minimum, configure the `COMMON` and `NETWORK` sections:

| Variable | Description |
|---|---|
| `DOMAIN` | Your domain name (e.g. `example.com`) |
| `EMAIL` | Email for Let's Encrypt certificate registration |
| `CF_DNS_TOKEN` | Cloudflare API token (create using the **Edit zone DNS** template) |
| `CF_GLOBAL_TOKEN` | Cloudflare Global API token |
| `DOMAIN_ZONE_ID` | Cloudflare Zone ID for your domain |
| `TIMEZONE` | Timezone (e.g. `Asia/Seoul`, `America/New_York`) |

## 2. Run Portainer

Initialize the infrastructure with:

```bash
make init
```

This command:
1. Creates the `ingress` Docker network shared by all stacks
2. Creates the `my-self-hosting-services` Docker volume
3. Deploys Portainer via `init.yaml`

Once running, open Portainer at `http://<hostname>:9000/` and create your admin account.

## 3. Deploy services via Portainer (recommended)

The recommended way to deploy services is through Portainer using your forked Git repository.

1. Open Portainer and go to **Stacks** -> **Add stack**
2. Select **Repository** as the build method
3. Enter your forked repository URL (e.g. `https://github.com/<your-username>/my-self-hosting-services`)
4. Set the **Compose path** to the stack file (e.g. `network.yaml`, `authentik.yaml`, `n8n.yaml`)
5. Add the environment variables from your `.env` file under **Environment variables**
6. Deploy the stack

This allows Portainer to pull and redeploy stacks directly from your repository when you push changes.

### Alternative: CLI deployment

```bash
STACK_NAME=network make service-up
STACK_NAME=authentik make service-up
STACK_NAME=n8n make service-up
```

Deploy in this order: **network** -> **authentik** -> other services.
