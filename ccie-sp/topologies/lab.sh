#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Find all clab yaml files in the current directory
shopt -s nullglob
LABS=( *.clab.yaml )

if [ ${#LABS[@]} -eq 0 ]; then
    echo -e "${RED}No .clab.yaml files found in this directory.${NC}"
    exit 1
fi

echo -e "${CYAN}=====================================${NC}"
echo -e "${CYAN}    CCIE SP Containerlab Manager     ${NC}"
echo -e "${CYAN}=====================================${NC}"
echo "1) Start (Deploy) a Lab"
echo "2) Stop (Destroy) a Lab"
echo "3) Inspect a Running Lab"
echo "4) Exit"
echo ""
read -p "Select an action [1-4]: " action

case $action in
    1|2|3)
        echo ""
        echo -e "${GREEN}Select the topology:${NC}"
        select lab in "${LABS[@]}"; do
            if [[ -n "$lab" ]]; then
                target_lab=$lab
                break
            else
                echo "Invalid selection. Please try again."
            fi
        done
        ;;
    4)
        echo "Exiting."
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid input. Exiting.${NC}"
        exit 1
        ;;
esac

echo ""
case $action in
    1)
        echo -e "${GREEN}Deploying $target_lab...${NC}"
        # Added --reconfigure to ensure clean starts if bouncing between labs
        sudo containerlab deploy -t "$target_lab" --reconfigure
        ;;
    2)
        echo -e "${RED}Destroying $target_lab...${NC}"
        # Added --cleanup to wipe out lingering state files
        sudo containerlab destroy -t "$target_lab" --cleanup
        ;;
    3)
        echo -e "${CYAN}Inspecting $target_lab...${NC}"
        sudo containerlab inspect -t "$target_lab"
        ;;
esac

