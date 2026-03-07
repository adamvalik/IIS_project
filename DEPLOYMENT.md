# Deployment Guide

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Nginx & Proxy Setup Explained](#nginx--proxy-setup-explained)
3. [Fresh VM Setup](#fresh-vm-setup)
4. [Seeding the Database](#seeding-the-database)

---

## Architecture Overview

```
Internet
   │
   │  :80 / :443
   ▼
┌──────────────────────────────────┐
│  nginx  (outer reverse proxy)    │  ← ports 80 & 443 on the host
│  image: nginx:stable-alpine      │
│  config: nginx/conf.d/app.conf   │
└───────────────┬──────────────────┘
                │ proxy_pass http://web-app:80
                ▼
┌──────────────────────────────────┐
│  web-app  (Vue SPA + inner nginx)│  ← internal port 80 only
│  build: web-app/Dockerfile       │
│  config: web-app/nginx.conf      │
│                                  │
│  GET /          → serves dist/   │
│  GET /api/*     → strips /api,   │
│                   proxy_pass ──► │
└───────────────────────┬──────────┘
                        │ proxy_pass http://backend:8000
                        ▼
┌──────────────────────────────────┐
│  backend  (FastAPI / uvicorn)    │  ← internal port 8000 only
│  build: backend/Dockerfile       │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│  certbot  (Let's Encrypt)        │  ← no ports; writes certs to shared volume
│  image: certbot/certbot          │    auto-renews every 12 h
└──────────────────────────────────┘

┌──────────────────────────────────┐
│  PostgreSQL database             │  ← separate VM / server
│  host: 10.0.1.4:5432             │    not managed by this compose file
└──────────────────────────────────┘
```

Only ports **80** and **443** are exposed to the internet. Ports 8000 (backend) and the inner web-app :80 are Docker-internal only.

---

## Nginx & Proxy Setup Explained

### Outer nginx (`nginx/conf.d/app.conf`)

This is the only service that faces the internet. It has two responsibilities:

**1. HTTP → HTTPS redirect (port 80)**

```nginx
server {
    listen 80;
    location /.well-known/acme-challenge/ { root /var/www/certbot; }
    location / { return 301 https://$host$request_uri; }
}
```

All plain HTTP traffic is permanently redirected to HTTPS, except Let's Encrypt ACME challenge requests (used during certificate issuance/renewal).

**2. SSL termination + proxy (port 443)**

```nginx
server {
    listen 443 ssl;
    ssl_certificate     /etc/letsencrypt/live/<domain>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<domain>/privkey.pem;

    location / {
        proxy_pass http://web-app:80;
    }
}
```

All HTTPS traffic is decrypted here and forwarded over plain HTTP to the `web-app` container on the internal Docker network. The `web-app` never deals with TLS.

### Inner nginx (`web-app/nginx.conf`)

Built into the `web-app` Docker image. Two jobs:

**1. Serve the Vue SPA**

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

`try_files` falls back to `index.html` for any path that doesn't match a static file, which is what Vue Router needs for client-side navigation (e.g. `/animals/3` is not a real file; nginx returns `index.html` and Vue handles the route).

**2. Proxy `/api/*` to the backend**

```nginx
location /api/ {
    proxy_pass http://backend:8000/;
}
```

The trailing slash on `proxy_pass` is important — nginx strips the `/api` prefix before forwarding. So a request for `/api/animals` reaches the FastAPI backend as `/animals`, matching its router exactly.

### Why this two-layer approach?

| Concern | Handled by |
|---|---|
| TLS / HTTPS | Outer nginx |
| Static file serving & SPA routing | Inner nginx (web-app) |
| Backend API proxying | Inner nginx (web-app) |
| Certificate renewal | Certbot (ACME webroot via outer nginx) |

Keeping TLS termination in a separate, dedicated container makes it easy to swap or update the cert config without touching the app containers.

### Shared volumes

```
./certbot/www  →  /var/www/certbot   (nginx + certbot)   ACME challenge files
./certbot/conf →  /etc/letsencrypt   (nginx + certbot)   certificates & config
./nginx/conf.d →  /etc/nginx/conf.d  (nginx)             nginx config
```

Certbot writes renewal tokens to `certbot/www`; the outer nginx serves them at `/.well-known/acme-challenge/` so Let's Encrypt can verify domain ownership.

---

## Fresh VM Setup

### Prerequisites

- Ubuntu 22.04 (or 24.04) VM
- Public DNS: `djkhaled-animal-shelter.switzerlandnorth.cloudapp.azure.com` pointing to the VM's IP
- Azure NSG inbound rules: **TCP 80**, **TCP 443**, **TCP 22** (your IP)
- The PostgreSQL database is already running on `10.0.1.4:5432`

### 1. Install Docker

```bash
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Allow running docker without sudo (re-login required)
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Clone the repository

```bash
git clone https://github.com/<your-org>/IIS_project.git
cd IIS_project
```

### 3. Configure secrets / environment

The `DATABASE_URL` is already set in `docker-compose.yml`. If you need to change it:

```bash
# Directly edit docker-compose.yml, or override via .env file at project root:
echo "DATABASE_URL=postgresql+psycopg2://user:password@10.0.1.4:5432/animal_shelter_db" >> .env
```

### 4. Issue the first TLS certificate and start services

Edit the email address in `init-letsencrypt.sh` (used for expiry notices):

```bash
nano init-letsencrypt.sh
# Change: EMAIL="your@email.com"
```

Then run it:

```bash
chmod +x init-letsencrypt.sh
./init-letsencrypt.sh
```

This script:
1. Creates `certbot/www` and `certbot/conf` directories
2. Downloads recommended TLS parameters from Certbot
3. Generates a temporary self-signed cert so nginx can start
4. Starts all Docker Compose services (`docker compose up --build -d`)
5. Deletes the temporary cert
6. Issues a real Let's Encrypt certificate via the ACME webroot challenge
7. Reloads nginx to load the real cert

After it completes, the app is live at `https://djkhaled-animal-shelter.switzerlandnorth.cloudapp.azure.com`.

### 5. Verify everything is running

```bash
docker compose ps
# All four services (backend, web-app, nginx, certbot) should show status "Up"

docker compose logs nginx   # check for SSL errors
docker compose logs backend # check DB connection
```

### Subsequent deploys

```bash
git pull
docker compose down
docker compose up --build -d
```

No need to re-run `init-letsencrypt.sh`. The `certbot` service renews the certificate automatically every 12 hours.

---

## Seeding the Database

`backend/example_data.py` populates the database with demo users, animals, medical records, examination requests, borrow slots, and reservations.

### Seed data created

| Entity | Details |
|---|---|
| Users | `admin@admin.com` / `admin123` (admin), `caregiver@example.com` / `caregiver123`, `vet@example.com` / `vet123`, `volunteer@example.com` / `volunteer123` (verified), `unverified@example.com` / `unverified123` |
| Animals | Bella (Dog), Mittens (Cat), Rabbie (Rabbit) — with photos from `backend/images/` |
| Medical records | 1 record for Bella |
| Examination requests | 2 requests (Bella + Mittens) |
| Borrow slots | 5 slots across Bella and Mittens |
| Reservations | 2 reservations (1 approved, 1 pending) |

### How to run the seed

The backend container has everything it needs. Run the script inside the running container:

```bash
docker compose exec backend python example_data.py
```

Expected output:
```
Example users added to the database.
Example animals added to the database.
Example examination requests added to the database.
Example medical records added to the database.
Example animal borrows added to the database.
Example reservations added to the database.
```

> **Warning:** Running the seed script more than once will create duplicate records (no idempotency check). If you need a clean re-seed, clear the relevant tables first or reset the database schema before re-running.

### Re-seeding on a clean database

If you need to reset and re-seed completely:

```bash
# Drop and recreate all tables, then re-seed
docker compose exec backend python -c "
from db import Base, engine
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print('Tables recreated.')
"

docker compose exec backend python example_data.py
```
