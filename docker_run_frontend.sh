#!/bin/bash

sudo docker run \
  --env MYSQL_HOST="mysql0.mateos.lan" \
  --env MYSQL_NAME="l4mbda" \
  --env MYSQL_USER="l4mbda" \
  --env MYSQL_PASSWORD="magnet in the shoe holE 123##" \
  --env REDIS_HOST="redis0.mateos.lan" \
  --env REDIS_PASSWORD="foobared" \
  -p 8080:8080 l4mbda-worker /app/frontend_start.sh
