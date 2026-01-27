# Register an App with Authentik

Repeat these steps for each service you want to protect with Authentik forward authentication.

## 1. Create a Proxy Provider

*The provider defines how to authenticate and which external host to protect.*

1. Go to authentik -> admin interface
2. Application -> Provider -> Create -> Select `Proxy Provider`
3. Configure:
   - Name: `service_name`
   - Authorization flow: `default-provider-authorization-explicit-consent (Authorize Application)`
   - Forward Auth (External Host): `https://service_name.<your-domain>`

## 2. Create an Application

*The application represents the service being protected and links to the provider.*

1. Application -> Application -> Create
2. Configure:
   - Name: `service_name`
   - Slug: `service_name`
   - Provider: `service_name` (select the provider created above)

## 3. Create/Configure Outpost

*The outpost is the forward auth middleware that enforces authentication. Create once and reuse for multiple services.*

1. Application -> Outposts -> Create (if not already created)
2. Configure:
   - Name: `ForwardAuth`
   - Type: `Proxy`
   - Applications: Select `service_name` (or multiple services)

If an outpost already exists, edit it and add the new application to its application list.

## 4. Deploy the Outpost

*Only required the first time you create the outpost.*

1. Click the outpost -> Click `Outpost Deployment Info`
2. Copy the `Authentik Token`
3. Add the token to your `.env` file as `AUTHENTIK_ACCESS_TOKEN` and redeploy the Authentik stack
