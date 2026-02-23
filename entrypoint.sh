#!/bin/bash
set -e

export PATH="$PATH:/usr/games"

echo "Updating Project Zomboid dedicated server..."
steamcmd +runscript /home/pzuser/update_zomboid.txt

echo "Starting Project Zomboid dedicated server..."
exec bash /opt/pzserver/start-server.sh "$@"
