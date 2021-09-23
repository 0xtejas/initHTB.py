# initHTB.py
This script helps us to add IP, host name entry in hosts file and create directory and much more features coming up!

# SETTING UP
1. You'll have to run this if you are not a root user `sudo chown $USER /etc/hosts`.
2. There is a template `hosts` file along with this, **please maintain the structure**.

# CONTRIBUTE

Please fork, contribute and make a pull request. If you have any issues with this project, please feel free to create issue.


1. Convert the existing code to class based
2. Use error handling 
3. Open new default terminal unless specified the terminal name in the `config.json`. 
    
    - If `config.json` has `tmux` set `True` then open the terminal in the `parent_directory` with tmux.
    and run `openvpn` in `window 1`. 
    - In `window 2` run `nmap scan` and `save the output`. - User can select the mode and can add modes too.
    - In `window 3` run `feroxbuster` or whichever. - user can select mode and can add modes too.


