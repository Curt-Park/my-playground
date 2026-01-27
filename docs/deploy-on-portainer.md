# Deploy a Stack on Portainer

The recommended way to deploy service stacks is through Portainer using your forked Git repository. This lets you manage stacks from the Portainer console and redeploy when you push changes to GitHub.

## Deploy a new stack

1. Open Portainer at `http://<hostname>:9000/` (or `https://portainer.<your-domain>/` after the network stack is deployed)
2. Go to **Stacks** -> **Add stack**
3. Enter a stack name (e.g. `network`, `authentik`, `n8n`)
4. Select **Repository** as the build method
5. Enter your forked repository URL (e.g. `https://github.com/<your-username>/my-self-hosting-services`)
6. Set **Compose path** to the stack file (e.g. `network.yaml`)
7. Under **Environment variables**, click **Advanced mode** and paste the contents of your `.env` file.
8. Click **Deploy the stack**

## Update a stack

After modifying a compose file in your repository:

1. Go to the stack in Portainer
2. Click **Pull and redeploy**

## Alternative: CLI deployment

```bash
STACK_NAME=<stack-name> make service-up    # deploy
STACK_NAME=<stack-name> make service-down  # tear down
```
