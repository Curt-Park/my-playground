# Cloudflare Setup

This project relies on Cloudflare for DNS management, SSL certificate issuance (via DNS-01 challenge), dynamic DNS updates, and proxied traffic for DDoS protection. You need to configure your Cloudflare account and create API tokens before deploying the network stack.

## 1. Get a domain

You need your own domain name before proceeding. Purchase one from a domain registrar (e.g. Namecheap, Google Domains, Cloudflare Registrar).

## 2. Add your domain to Cloudflare

See also: [Cloudflare - Add a site](https://developers.cloudflare.com/fundamentals/manage-domains/add-site/)

1. Sign up or log in at [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Select **Onboard a domain**
3. Enter your apex domain (e.g. `example.com`) and proceed
4. Select a plan (Free plan works)
5. Review the DNS records Cloudflare found via automatic scan — verify they are correct and add any missing records
6. If DNSSEC is enabled at your registrar, disable it before changing nameservers
7. Update your domain registrar's nameservers to the two nameservers Cloudflare assigns
8. Wait for nameserver propagation (can take up to 24 hours)

## 3. Get the Zone ID

See also: [Cloudflare - Find zone and account IDs](https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/)

1. Go to your domain's **Overview** page in the Cloudflare Dashboard
2. Scroll down to the **API** section on the right sidebar
3. Find **Zone ID** and select **Click to copy**
4. Set it as `DOMAIN_ZONE_ID` in your `.env` file

## 4. Create API tokens

See also: [Cloudflare - Create an API token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/), [Cloudflare - API keys](https://developers.cloudflare.com/fundamentals/api/get-started/keys/)

Two tokens are needed: a scoped **DNS API token** and a **Global API key**.

### DNS API Token (`CF_DNS_TOKEN`)

Used by Traefik for Let's Encrypt DNS-01 challenge and by cloudflare-ddns for dynamic DNS updates.

1. Go to **My Profile** -> [**API Tokens**](https://dash.cloudflare.com/profile/api-tokens)
2. Click **Create Token**
3. Use the **Edit zone DNS** template
4. Configure permissions:
   - Zone / Zone / Read
   - Zone / DNS / Edit
5. Set **Zone Resources** to your specific domain
6. Create the token and copy it immediately — the token secret is **only shown once**
7. Set it as `CF_DNS_TOKEN` in your `.env`

### Global API Key (`CF_GLOBAL_TOKEN`)

Used by traefik-cloudflare-companion to automatically create DNS records for new services.

1. Go to **My Profile** -> [**API Tokens**](https://dash.cloudflare.com/profile/api-tokens)
2. Scroll down to the **API Keys** section
3. Click **View** next to **Global API Key**
4. Copy the key and set it as `CF_GLOBAL_TOKEN` in your `.env`

> **Note:** The Global API Key grants unrestricted access to your entire Cloudflare account and cannot be scoped. traefik-cloudflare-companion requires it because it does not support scoped API tokens. Keep this key secure and do not share it.

## 5. Configure SSL/TLS mode

See also: [Cloudflare - SSL/TLS encryption modes](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/)

Traefik terminates TLS with a Let's Encrypt wildcard certificate. To avoid redirect loops, the Cloudflare SSL mode must match.

1. Go to your domain in the Cloudflare Dashboard
2. Navigate to **SSL/TLS** -> **Overview**
3. Set the encryption mode to **Full (strict)**

This ensures Cloudflare connects to your origin over HTTPS and validates the certificate issued by Let's Encrypt. Do not use **Flexible** mode — it connects to your origin over HTTP, which causes infinite redirect loops with Traefik's HTTP-to-HTTPS redirection.

## 6. Environment variable summary

| Variable | Where to find | Used by |
|---|---|---|
| `DOMAIN` | Your registered domain | All services |
| `EMAIL` | Your Cloudflare account email | Traefik (Let's Encrypt), cloudflare-companion |
| `CF_DNS_TOKEN` | API Tokens -> Edit zone DNS template | Traefik (DNS-01 challenge), cloudflare-ddns |
| `CF_GLOBAL_TOKEN` | API Tokens -> Global API Key | cloudflare-companion |
| `DOMAIN_ZONE_ID` | Domain Overview -> API section | cloudflare-companion |

## How it all works together

- **Traefik** uses `CF_DNS_TOKEN` to solve DNS-01 challenges and obtain a wildcard certificate (`*.your-domain`) from Let's Encrypt. It also trusts [Cloudflare's IP ranges](https://www.cloudflare.com/ips/) for forwarded headers.
- **cloudflare-companion** watches Docker for containers with Traefik labels and automatically creates CNAME records in Cloudflare pointing to your domain, with proxy enabled.
- **cloudflare-ddns** updates the root domain's DNS A record to your current public IP, keeping your homelab accessible even when your ISP changes your IP address.
