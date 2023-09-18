#!/bin/bash
# start Docker daemon
sudo systemctl start docker

# build the Docker image
docker build -t openaichat .

# run the Docker container
docker run -p 4000:80 openaichat
