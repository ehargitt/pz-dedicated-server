#!/bin/bash
# The commands for this script were pulled from:
# https://pzwiki.net/wiki/Dedicated_server#Linux
# Run this script using `sudo`

# Don't run the server as root. Add a user such as pzuser
sudo adduser pzuser
# Temporarily give sudo privilages
sudo usermod -aG sudo pzuser

# Run subsequent commands as the steam user
sudo -u pzuser bash << 'EOF'
	# Go into its home folder
	cd $HOME

	# To install SteamCMD, add the non-free repository, and enable x86 packages
	sudo add-apt-repository -y multiverse
	sudo dpkg --add-architecture i386
	sudo apt update
	sudo apt install -y steamcmd
EOF

# Revoke sudo privilages
sudo deluser pzuser sudo

# We will install Zomboid Server in /opt/pzserver
sudo mkdir -p /opt/pzserver
sudo chown pzuser:pzuser /opt/pzserver

# Open the ports
sudo ufw allow 16261/udp
sudo ufw allow 16262/udp
# Reload the firewall to make the added rules go into effect
sudo ufw reload

sudo cp ./update_zomboid.txt ~pzuser

# Log in as pzuser and execute subsequent commands as pzuser
sudo runuser -l pzuser -c 'steamcmd +runscript $HOME/update_zomboid.txt'
