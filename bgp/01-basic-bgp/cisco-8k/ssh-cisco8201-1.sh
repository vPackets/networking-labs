#!/bin/bash

# WARNING: Storing passwords in plaintext scripts is insecure. Use this for lab purposes only.

# Server credentials
SERVER_IP="clab-eBGP-c8K-Cisco8201-1"
USERNAME="cisco"
PASSWORD="cisco123"

# Command to connect to the server
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no $USERNAME@$SERVER_IP

# If you need to run a specific command on the remote server, you can do so like this:
# sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no $USERNAME@$SERVER_IP "<command_to_run>"

