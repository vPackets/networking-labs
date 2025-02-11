#!/bin/bash

while true; do
    echo "Which router do you want to ssh into?"
    echo "1) Router 1"
    echo "2) Router 2"
    echo "0) Exit"
    echo "Enter the number (e.g., 1):"
    read router_choice

    USERNAME="cisco"
    PASSWORD="cisco123"

    case $router_choice in
        1|01)
            SERVER_IP="clab-eBGP-C8K-Cisco8201-1"
            ;;
        2|02)
            SERVER_IP="clab-eBGP-C8K-Cisco8201-2"
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

    # Use sshpass to SSH into the selected router
    sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no $USERNAME@$SERVER_IP

    echo "SSH session has ended. You can choose another router or exit."
done






