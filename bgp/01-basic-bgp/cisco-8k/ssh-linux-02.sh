#!/bin/bash

# Define the container name as a variable for easy modification
CONTAINER_NAME="clab-eBGP-c8K-linux02"

# Check if the specified Docker container is running
if [ "$(docker ps -q -f name=^/${CONTAINER_NAME}$)" ]; then
    # If the container is running, execute a Bash shell inside it
    docker exec -it "$CONTAINER_NAME" bash
else
    echo "Container '${CONTAINER_NAME}' is not running."
    echo "Please start the container and try again."
fi

