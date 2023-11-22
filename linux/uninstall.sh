#!/bin/bash

# Confirmation prompt
read -p "This will uninstall Project Zomboid Server and remove the user 'pzuser'. Are you sure? (y/n): " answer

# Check the user's response
if [[ "$answer" != "y" ]]; then
    echo "Uninstallation aborted."
    exit 0
fi

# Remove the Zomboid Server installation
sudo rm -rf /opt/pzserver

# Remove the user "pzuser" and their home directory
sudo userdel -r pzuser

# Remove firewall rules for Zomboid Server ports
sudo ufw delete allow 16261/udp
sudo ufw delete allow 16262/udp
sudo ufw reload

echo "Project Zomboid Server has been uninstalled, and user 'pzuser' has been removed."