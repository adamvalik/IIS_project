#!/bin/bash
# First-time Let's Encrypt certificate setup.
# Run this ONCE on the VM after cloning the repo.
# After this, certbot auto-renews every 12 h via the certbot service.

set -e

DOMAIN="djkhaled-animal-shelter.switzerlandnorth.cloudapp.azure.com"
EMAIL="your@email.com"   # <-- CHANGE THIS to a real address for expiry notices
RSA_KEY_SIZE=4096
CERT_PATH="./certbot/conf/live/${DOMAIN}"

echo "### Creating required directories..."
mkdir -p ./certbot/www ./certbot/conf

echo "### Downloading recommended TLS parameters..."
if [ ! -e "./certbot/conf/options-ssl-nginx.conf" ]; then
  curl -fsSL https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf \
    -o ./certbot/conf/options-ssl-nginx.conf
fi
if [ ! -e "./certbot/conf/ssl-dhparams.pem" ]; then
  curl -fsSL https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem \
    -o ./certbot/conf/ssl-dhparams.pem
fi

echo "### Creating temporary self-signed certificate so nginx can start..."
mkdir -p "${CERT_PATH}"
docker compose run --rm --entrypoint "openssl req -x509 -nodes -newkey rsa:${RSA_KEY_SIZE} -days 1 \
  -keyout /etc/letsencrypt/live/${DOMAIN}/privkey.pem \
  -out /etc/letsencrypt/live/${DOMAIN}/fullchain.pem \
  -subj '/CN=${DOMAIN}'" certbot

echo "### Starting all services (build if needed)..."
docker compose up --build -d

echo "### Waiting for nginx to be ready (5s)..."
sleep 5

echo "### Removing temporary certificate..."
docker compose run --rm --entrypoint \
  "rm -rf /etc/letsencrypt/live/${DOMAIN} \
          /etc/letsencrypt/archive/${DOMAIN} \
          /etc/letsencrypt/renewal/${DOMAIN}.conf" certbot

echo "### Requesting real Let's Encrypt certificate..."
docker compose run --rm --entrypoint "certbot certonly \
  --webroot -w /var/www/certbot \
  --email ${EMAIL} \
  --agree-tos \
  --no-eff-email \
  -d ${DOMAIN}" certbot

echo "### Reloading nginx to load the real certificate..."
docker compose exec nginx nginx -s reload

echo ""
echo "All done! Your app is live at https://${DOMAIN}"
echo "The certbot service will auto-renew the certificate every 12 hours."
