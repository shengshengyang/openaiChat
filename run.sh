#!/bin/bash
# Build the Docker image
docker build -t openaichat .

# Run the Docker container
docker run -d -p 80:80 openaiChat