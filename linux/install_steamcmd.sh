#!/bin/bash
# The commands for this script were pulled from:
# https://developer.valvesoftware.com/wiki/SteamCMD#Ubuntu
# Run this script using `sudo`

# As the root user, create the steam user
sudo useradd -m steam
sudo passwd steam

# Run subsequent commands as the steam user
sudo -u steam bash << EOF
	# Go into its home folder
	cd /home/steam

	# To install SteamCMD, add the non-free repository, and enable x86 packages
	sudo add-apt-repository multiverse
	sudo dpkg --add-architecture i386
	sudo apt update
	sudo apt install steamcmd
EOF