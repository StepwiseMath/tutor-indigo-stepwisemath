#!/bin/bash

# Stop all running containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images forcefully
docker rmi -f $(docker images -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)

# Prune the system to remove any dangling resources
docker system prune -a --volumes -f

echo "Docker environment has been completely reset."
