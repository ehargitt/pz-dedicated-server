#!/bin/bash
# The commands for this script were pulled from:
# https://pzwiki.net/wiki/Dedicated_server#Linux
# Run this script using `sudo`

# Don't run the server as root. Add a user such as pzuser
adduser --disabled-password pzuser

# We will install Zomboid Server in /opt/pzserver
mkdir /opt/pzserver
chown pzuser:pzuser /opt/pzserver

# Open the ports
sudo ufw allow 16261/udp
sudo ufw allow 16262/udp
# Reload the firewall to make the added rules go into effect
sudo ufw reload

# Log in as pzuser and execute subsequent commands as pzuser
sudo -u pzuser -i <<EOF
    # Create the configuration file /home/pzuser/update_zomboid.txt that will manage steamcmd
    cat >$HOME/update_zomboid.txt <<'EOL'
    // update_zomboid.txt
    //
    @ShutdownOnFailedCommand 1 //set to 0 if updating multiple servers at once
    @NoPromptForPassword 1
    force_install_dir /opt/pzserver/
    //for servers which don't need a login
    login anonymous 
    app_update 380870 validate
    quit
    EOL

    # Now install Project Zomboid Server. You will use this same command every time
    # you want to update the server to the latest version.
    steamcmd +runscript $HOME/update_zomboid.txt
EOF
