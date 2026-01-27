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

## 3. Deploy service stacks

After Portainer is running, deploy stacks following the [deploy on Portainer](deploy-on-portainer.md) guide.

Deploy in this order: **network** -> **authentik** -> other services.
