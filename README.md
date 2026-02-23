# pz-dedicated-server

Docker setup for hosting a Project Zomboid Build 42 (unstable beta) dedicated server.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (included with Docker Desktop)

## Quick Start

Build the image:

```bash
docker compose build
```

Start the server:

```bash
docker compose up -d
```

## First Run — Set Admin Password

On the first start, the server will prompt you to set the admin password. Attach to the container to interact with the console:

```bash
docker attach pzserver
```

Set the password when prompted. To detach without stopping the server, press `Ctrl+P` then `Ctrl+Q`.

## Usage

**View logs:**

```bash
docker compose logs -f
```

**Stop the server:**

```bash
docker compose down
```

**Restart the server (preserves saves and config):**

```bash
docker compose down && docker compose up -d
```

**Force update the server (rebuilds the image):**

```bash
docker compose build --no-cache && docker compose up -d
```

**Pass arguments to the server** (e.g. custom server name):

```bash
docker compose run --rm --service-ports pzserver -servername MyServer
```

## Server Configuration

Server config files and saves are stored in the `pzserver-config` Docker volume, which maps to `/home/pzuser/Zomboid` inside the container.

To edit server settings, find the config files in the volume:

```bash
docker compose exec pzserver ls /home/pzuser/Zomboid/Server
```

## Data Persistence

Two named volumes keep your data safe across restarts and rebuilds:

| Volume | Container Path | Contents |
|---|---|---|
| `pzserver-data` | `/opt/pzserver` | Server binary files (avoids re-downloading) |
| `pzserver-config` | `/home/pzuser/Zomboid` | Saves, config, logs |

## Ports

| Port | Protocol | Purpose |
|---|---|---|
| 16261 | UDP | Game traffic |
| 16262 | UDP | Game traffic |

## How to Connect

1. Note the IP address of the host machine.
2. Start Project Zomboid and click **Join**.
3. Enter the server IP and port (default 16261).
4. To log in as admin, use `admin` as the username and the password you set on first run.
