#!/bin/bash

domains=(itformhelp.ru www.itformhelp.ru)
email="admin@itformhelp.ru"
staging=0 # Set to 1 if you're testing your setup

# Create dummy certificates
path="/etc/letsencrypt/live/$domains"
docker compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:4096 -days 1\
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" certbot

echo "### Starting nginx ..."
docker compose up --force-recreate -d frontend

echo "### Deleting dummy certificate ..."
docker compose run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/$domains && \
  rm -Rf /etc/letsencrypt/archive/$domains && \
  rm -Rf /etc/letsencrypt/renewal/$domains.conf" certbot

echo "### Requesting Let's Encrypt certificate ..."
docker compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/html \
    --email $email \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    ${staging:+--staging}" certbot

echo "### Reloading nginx ..."
docker compose exec frontend nginx -s reload
