#!/bin/bash

while true; do
echo "Which container do you want to connect to?"
echo "1) Linux ISP 01"
echo "2) Linux ISP 02"
echo "0) Exit"
echo "Enter the number (e.g., 1):"
read container_choice

case $container_choice in
    1|01)
        CONTAINER_NAME="clab-eBGP-CSR-linux01"
        ;;
    2|02)
        CONTAINER_NAME="clab-eBGP-CSR-linux02"
        ;;
    0|exit)
            echo "Exiting."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            continue
            ;;
esac

# Use docker exec to start a bash shell in the selected container
docker exec -it $CONTAINER_NAME bash

    echo "SSH session has ended. You can choose another router or exit."
done

# Note: This script assumes you have permissions to run docker commands without sudo.
# If not, you might need to prefix `docker exec` with `sudo` or adjust your user permissions.
