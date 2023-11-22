#!/bin/bash

# Log in as pzuser and execute subsequent commands as pzuser
sudo runuser -l pzuser -c '/opt/pzserver/start-server.sh'