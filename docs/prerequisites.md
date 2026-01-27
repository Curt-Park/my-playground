# Prerequisites

## Docker and Docker Compose

Docker Compose is required to deploy all services. It comes bundled with Docker Desktop.

### macOS

Install Docker Desktop via Homebrew:

```bash
brew install --cask docker
```

Or download from the [official website](https://docs.docker.com/desktop/setup/install/mac-install/).

### Linux

Install Docker Engine and the Compose plugin:

```bash
# Add Docker's official GPG key and repository
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

For other distributions, see the [Docker Engine installation docs](https://docs.docker.com/engine/install/).

### Verify installation

```bash
docker compose version
```

## Fork the repository

Fork this repository to your own GitHub account. Portainer can pull stack definitions directly from a Git repository, so having your own fork allows you to manage and customize configurations through version control.

1. Click **Fork** on the repository page
2. Clone your fork locally:
   ```bash
   git clone https://github.com/<your-username>/my-self-hosting-services.git
   cd my-self-hosting-services
   ```
