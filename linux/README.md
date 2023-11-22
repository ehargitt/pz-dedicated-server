# Supported OSs
Only Ubuntu.

# Installation steps
Take these steps if this is the first time you are running a PZ server on this machine.
0. Run `sudo install.sh`.

# Starting the server
You can start the server by running `./start.sh`. The first time you start you will be prompted to set the password for the 'admin' user. Note the password and do not share it. This is how you will do admin stuff in-game.

# Stopping the server
You can stop the server by giving the `quit` command in the same terminal window that the server is running.

# Uninstallation steps
0. Make sure the server is stopped. See the "Stopping the server" section in this README.
1. Run `sudo ./uninstall.sh` and follow the prompts.

# How to connect to the server on the LAN
0. Note the IPv4 address of your machine. You can find this by running `ifconfig`. It is likely the address starting with `192.168.xxx.xxx`.
1. Make sure the server is running.
2. Start the Project Zomboid game client and click `Join`.
3. Enter the server details. If you want to login as the admin, use `admin` as the username and the password you set during the first-time server start up.