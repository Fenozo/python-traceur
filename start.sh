#!/bin/bash

git pull
docker compose up -d
docker exec -it  traceur_b bash