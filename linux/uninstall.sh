#!/bin/bash

# Confirmation prompt
read -p "This will uninstall Project Zomboid Server and remove the user 'pzuser'. Are you sure? (y/n): " answer

# Check the user's response
if [[ "$answer" != "y" ]]; then
    echo "Uninstallation aborted."
    exit 0
fi

# Stop the Zomboid Server if it's running
sudo systemctl stop pzserver.service  # Assuming you have a service file for pzserver

# Remove the Zomboid Server installation
rm -rf /opt/pzserver

# Remove the user "pzuser" and their home directory
userdel -r pzuser

# Remove firewall rules for Zomboid Server ports
sudo ufw delete allow 16261/udp
sudo ufw delete allow 16262/udp
sudo ufw reload

echo "Project Zomboid Server has been uninstalled, and user 'pzuser' has been removed."