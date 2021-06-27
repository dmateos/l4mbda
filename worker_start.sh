#!/bin/bash

cd /app

celery -A jobmanager.tasks worker -c 2 --max-tasks-per-child 100

while true; do
  sleep 10
done
