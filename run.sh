#!/bin/bash

# Stop the existing Docker container running on port 80
docker stop $(docker ps -q --filter "publish=4000")

# Remove the existing Docker container running on port 80
docker rm $(docker ps -aq --filter "publish=4000")

# build the Docker image
docker build -t openaichat .

# run the Docker container and log its output
docker run -d -p 4000:4000 openaichat >> app.log
