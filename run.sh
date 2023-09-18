#!/bin/bash

# start Docker daemon
sudo systemctl start docker

# remove unused Docker objects
docker system prune -a -f

# build the Docker image
docker build -t openaichat .

# run the Docker container and log its output
docker run -p 4000:4000 openaichat >> app.log
