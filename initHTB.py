#!/usr/bin/env python3

import argparse,json,os
import libtmux
import getpass
import time 

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
        self.parentDirectory = self.config['directory'][0]['parentDirectory'].replace('\"$USER\"', os.environ['USER'])
        self.openvpnDirectory = self.config['directory'][1]['openvpnDirectory']
        self.VHOST=VHOST
        self.IP=IP
    
    def initialize(self):
        try:
            path = os.path.join(self.parentDirectory,self.VHOST)
            os.mkdir(path)
            print(terminalColors.SUCESS + "[+] Directory '% s' created" % self.VHOST + terminalColors.ENDC)

        except Exception:
            print(terminalColors.FAIL + "[-] Directory '% s' already exists" % self.VHOST + terminalColors.ENDC)
            

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
            path = os.path.join(f'{self.parentDirectory}',f'{self.VHOST}')
            os.system(f"tmux new-session -t {self.VHOST} -d -c {path}")
            tmux = libtmux.Server()
            print(terminalColors.SUCESS + "[+] Terminal shell created" + terminalColors.ENDC)
            print(terminalColors.INFO + "[+] Connecting to OPENVPN" + terminalColors.ENDC)
            self.session = tmux.get_by_id('$0')
            window = self.session.select_window(0)
            window.rename_window('openvpn')
            pane = window.select_pane(0)
            pane.send_keys(f"sudo openvpn {self.openvpnDirectory}", enter=True)
            print("Enter the password for SUDO")
            self.password = getpass.getpass()
            pane.send_keys(self.password, enter=True ,suppress_history=False)
            print(terminalColors.SUCESS + "[+] OPENVPN CONNECTED" + terminalColors.ENDC)
            print(terminalColors.SUCESS + "[+] Terminal shell created!" + terminalColors.ENDC)
        except Exception:
            print(terminalColors.FAIL + "[-] Error while creating terminal shell" + terminalColors.ENDC)
    
    
    def runNmap(self,option=0):
        try:
            self.session.new_window(window_name='nmap')
            window = self.session.select_window(1)
            pane = window.select_pane(0)
        except Exception:
            print("Error!")

        try:
            command = self.config['toolCommand'][0]['nmap'][option][f"{option}"].replace("$VHOST",self.VHOST.lower() + '.htb')
            pane.send_keys(command, enter=True)
            print(terminalColors.INFO + "[+] Sleeping 10 seconds.... Waiting for OPENVPN TO CONNECT!" + terminalColors.ENDC)
            time.sleep(10)
            pane.send_keys(self.password, enter=True, suppress_history=False) 
        except:
            print(terminalColors.FAIL + "[-] Command option chosen is not found!" + terminalColors.ENDC)
            print(terminalColors.INFO + "[*] Please check the config file, Running default scan" + terminalColors.ENDC)
            command = self.config['toolCommand'][0]['nmap'][0][0].replace("$VHOST",f"{self.VHOST}")
            pane.send_keys(command, enter=True)
            pane.send_keys(self.password, enter=True, suppress_history=False)
            print(terminalColors.SUCESS + "[+] Default scan is done!" + terminalColors.ENDC)
    
    def terminalSession(self):
        self.session.attach_session()

def create_directory(config):
    try:
        path = config['directory'][0]['parentDirectory'].replace('\"$USER\"', os.environ['USER'])
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
    parser.add_argument("-N", "--nmap", help="""
    Enter the command number to run you can also add add multiple command numbers separated by comma 
    Default command is set to 0.
    """, action='store_true')
    parser.add_argument("-dN", "--dnmap", help="To disable nmap scan", action='store_true')


    args = parser.parse_args()

    if args.initialize:
        with open('config.json') as file:
            config = json.load(file)
        create_directory(config)
    elif bool(args.ip) ^ bool(args.name):
        parser.error(terminalColors.FAIL + "--ip and --vhost must be used together" + terminalColors.ENDC)
    elif bool(args.ip) ^ bool(args.name) ^ bool(args.nmap):
        parser.error(terminalColors.FAIL + "--ip and --vhost and --nmap must be used together" + terminalColors.ENDC)
    elif args.ip and args.name:
        with open('config.json') as file:
            config = json.load(file)
        initHTB = initHTB(config,args.ip,args.name)
        initHTB.initialize()
        initHTB.create_terminal_shell()
        if args.nmap == False:
            initHTB.runNmap()
        if args.nmap == True:
            initHTB.runNmap(args.nmap)
        
        initHTB.terminalSession()
     