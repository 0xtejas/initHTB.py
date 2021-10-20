[![CodeQL](https://github.com/cognizance-amrita/initHTB.py/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/cognizance-amrita/initHTB.py/actions/workflows/codeql-analysis.yml)
# initHTB.py

```
 _       _ _           _____  ___ 
(_)_ __ (_) |_  /\  /\/__   \/ __\
| | '_ \| | __|/ /_/ /  / /\/__\//
| | | | | | |_/ __  /  / / / \/  \
|_|_| |_|_|\__\/ /_/   \/  \_____/              
                                   py
```


This script helps us to add IP, host name entry in hosts file and create directory run nmap scan and directory scan with your favourite tools. 
More commands will be available, as you create issue.

# SETTING UP

1. You'll have to run this if you are not a root user `sudo chown $USER /etc/hosts`.
2. There is a template `hosts` file along with this, **please maintain the structure**.
3. *Optionally* create a virtualenv with `virtualenv . && . ./bin/activate`
4. Install dependencies with `pip install -r requirements.txt`
5. Run `python initHTB.py`
# USAGE
1. Edit `config.json` and set  the `parentDirectory` and `openvpnDirectory` keys to your desired working directory, and OpenVPN config path respectively.
2. Run `python3 initHTB.py -I` to create the `parentDirectory` specified above. `$USER` in the path will be replaced with the current logged in username.
3. Run `python3 initHTB-py -i <IP address> -n <name of HTB box>`. At least `-i` and `-n` must be provided. Optionally `-N` can be used to set the nmap command to run, specified in `config.json`.

Run `python3 initHTB.py -h` for help
```
(_)_ __ (_) |_  /\  /\/__   \/ __\
| | '_ \| | __|/ /_/ /  / /\/__\//
| | | | | | |_/ __  /  / / / \/  \
|_|_| |_|_|\__\/ /_/   \/  \_____/
                                  py


usage: initHTB.py [-h] [-i IP] [-n NAME] [-I] [-N] [-dN]

optional arguments:
  -h, --help            show this help message and exit
  -i IP, --ip IP        IP of the VHOST
  -n NAME, --name NAME  BOX NAME
  -I, --initialize      Initialize the initHTB.py script
  -N, --nmap            Enter the command number to run you can also add add multiple command numbers separated by comma Default command is set to 0.
  -dN, --dnmap          To disable nmap scan

```



# SCREENSHOTS

![image](https://user-images.githubusercontent.com/47889755/134817046-3dc10a9a-f35b-4bff-9a06-bb5c4bbfe878.png)
![image](https://user-images.githubusercontent.com/47889755/134817067-008aa46a-2f54-4c26-9283-92daf7882ba5.png)
![image](https://user-images.githubusercontent.com/47889755/134817077-217372dd-8693-442e-86db-3772c997adbd.png)
![image](https://user-images.githubusercontent.com/47889755/134817079-07f3fa56-7590-4d26-b986-44f37838b12f.png)


# CONTRIBUTE

Please fork, contribute and make a pull request. If you have any issues with this project, please feel free to create issue.


# CREDITS

Thanks to [Libtmux](https://github.com/tmux-python/libtmux) a python API for TMUX. Without which this project would not been easy to work with.


---

**NOTE** ALWAYS DOWNLOAD FROM RELEASES for using the tool. I won't guarantee cloning the repo will work for usage. As there are breaking changes pushed frequently. 

