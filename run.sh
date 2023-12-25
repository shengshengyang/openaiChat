#!/bin/bash

# Stop the existing Docker container running on port 80
docker stop $(docker ps -q --filter "publish=8083")

# Remove the existing Docker container running on port 80
docker rm $(docker ps -aq --filter "publish=8083")

# start Docker daemon
sudo systemctl start docker

# remove unused Docker objects
docker system prune -a -f

# build the Docker image
docker build -t openaichat .

# run the Docker container and log its output
docker run -p 8083:8083 openaichat >> app.log
