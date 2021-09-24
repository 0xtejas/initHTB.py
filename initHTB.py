#!/usr/bin/env python3

import argparse,json,os
import libtmux
import getpass

# TERMINAL COLORS - CODE FROM https://stackoverflow.com/a/287944/11561065
class terminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    INFO = '\033[96m'
    SUCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(terminalColors.FAIL + " _       _ _           _____  ___" + terminalColors.ENDC) 
print(terminalColors.FAIL + "(_)_ __ (_) |_  /\  /\/__   \/ __\\" + terminalColors.ENDC)
print(terminalColors.FAIL + "| | '_ \| | __|/ /_/ /  / /\/__\//" + terminalColors.ENDC)
print(terminalColors.FAIL + "| | | | | | |_/ __  /  / / / \/  \\" + terminalColors.ENDC)
print(terminalColors.FAIL + "|_|_| |_|_|\__\/ /_/   \/  \_____/" + terminalColors.ENDC)
print(terminalColors.FAIL + "                                  py" + terminalColors.ENDC)
print("\n")

                                

class initHTB:
    def __init__(self, config,IP,VHOST):
        self.config = config
        self.tmux = self.config['tmux']
        self.terminal = self.config['terminal']
        self.parent_directory = self.config['parent_directory'].replace('\"$USER\"', os.environ['USER'])
        
        self.VHOST=VHOST
        self.IP=IP
    
    def initialize(self):
        try:
            path = os.path.join(self.parent_directory,self.VHOST)
            os.mkdir(path)
            print(terminalColors.SUCESS + "[+] Directory '% s' created" % self.VHOST + terminalColors.ENDC)

        except Exception as e:
            print(terminalColors.FAIL + "[-] Directory '% s' already exists" % self.VHOST + terminalColors.ENDC)
            print(e)

        with open('/etc/hosts','r') as file:
            content = file.read()

            new_content = content.replace("\n\n",f"\n{self.IP}    {self.VHOST.lower()}.htb\n\n",1)
        try:
            with open('/etc/hosts','w') as file:
                file.write(new_content)

            print(terminalColors.SUCESS + f"[+] IP: {self.IP} and HOST: {self.VHOST.lower()}.htb is added to the file!" + terminalColors.ENDC)
        except:
            print(terminalColors.FAIL + "[-] Error while writing to file" + terminalColors.ENDC)
            print(terminalColors.FAIL + "[-] Please check the file permissions" + terminalColors.ENDC)
            print(terminalColors.INFO + "[*] try running sudo chown % s /etc/hosts and then run this script" %os.environ['USER'] + terminalColors.ENDC)


    def create_terminal_shell(self):
        try:
            # CREATE A TERMINAL SHELL 
            print(terminalColors.INFO + "[+] Creating a terminal shell" + terminalColors.ENDC)
            path = os.path.join(f'{self.parent_directory}',f'{self.VHOST}')
            os.system(f"tmux new-session -t {self.VHOST} -d -c {path}")
            tmux = libtmux.Server()
            print(terminalColors.SUCESS + "[+] Terminal shell created" + terminalColors.ENDC)
            print(terminalColors.INFO + "[+] Connecting to OPENVPN" + terminalColors.ENDC)
            session = tmux.get_by_id('$0')
            window = session.select_window(0)
            pane = window.select_pane(0)
            pane.send_keys(f"sudo openvpn ~/Downloads/lab_TheWeeknd.ovpn", enter=True)
            print("Enter the password for SUDO")
            p = getpass.getpass()
            pane.send_keys(p, enter=True ,suppress_history=False)
            print(terminalColors.SUCESS + "[+] OPENVPN CONNECTED" + terminalColors.ENDC)
            pane.window.session.attach_session()
            
           
            

            print(terminalColors.SUCESS + "[+] Terminal shell created!" + terminalColors.ENDC)
        except Exception as e:
            print(terminalColors.FAIL + "[-] Error while creating terminal shell" + terminalColors.ENDC)
            print(e)



def create_directory(config):
    try:
        path = config['parent_directory'].replace('\"$USER\"', os.environ['USER'])
        os.makedirs(path)
        print(terminalColors.SUCESS + "[+] Directory Created as per config.json"  + terminalColors.ENDC)
    except OSError:
        print(terminalColors.FAIL + OSError + terminalColors.ENDC)
        print(OSError)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="IP of the VHOST")
    parser.add_argument("-n", "--name", help="BOX NAME")
    parser.add_argument("-I", "--initialize", help="Initialize the initHTB.py script", action='store_true')
    args = parser.parse_args()

    if args.initialize:
        with open('config.json') as file:
            config = json.load(file)
        create_directory(config)
    elif bool(args.ip) ^ bool(args.name):
        parser.error(terminalColors.FAIL + "--ip and --vhost must be used together" + terminalColors.ENDC)

    elif args.ip and args.name:
        with open('config.json') as file:
            config = json.load(file)
        initHTB = initHTB(config,args.ip,args.name)
        initHTB.initialize()
        initHTB.create_terminal_shell()
     