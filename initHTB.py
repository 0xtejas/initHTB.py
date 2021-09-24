#!/usr/bin/env python3

import os
import subprocess
import json
import sys 

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



class initHTB:
    def __init__(self, config):
        self.config = config
        self.tmux = self.config['tmux']
        self.terminal = self.config['terminal']
        self.parent_directory = self.config['parent_directory'].replace('\"$USER\"', os.environ['USER'])
        
        self.directory=input("Enter the Machine Name: ")
        self.ip=input("Enter the IP: ")
    
    def initialize(self):
        try:
            path = os.path.join(self.parent_directory,self.directory)
            os.mkdir(path)
            print(terminalColors.SUCESS + "[+] Directory '% s' created" % self.directory + terminalColors.ENDC)

        except OSError:
            print(terminalColors.FAIL + "[-] Directory '% s' already exists" % self.directory + terminalColors.ENDC)
    

        with open('/etc/hosts','r') as file:
            content = file.read()

            new_content = content.replace("\n\n",f"\n{self.ip}    {self.directory.lower()}.htb\n\n",1)
        try:
            with open('/etc/hosts','w') as file:
                file.write(new_content)

            print(terminalColors.SUCESS + f"[+] IP: {self.ip} and HOST: {self.directory.lower()}.htb is added to the file!" + terminalColors.ENDC)
        except:
            print(terminalColors.FAIL + "[-] Error while writing to file" + terminalColors.ENDC)
            print(terminalColors.FAIL + "[-] Please check the file permissions" + terminalColors.ENDC)
            print(terminalColors.INFO + "[*] try running sudo chown % s /etc/hosts and then run this script" %os.environ['USER'] + terminalColors.ENDC)

    def create_directory(self):
        try:
            path = os.path.join(self.parent_directory,self.directory)
            os.makedirs(path)
            print(terminalColors.SUCESS + "[+] Hirearchy Created as per config.json" % self.directory + terminalColors.ENDC)
            print(terminalColors.SUCESS + "[+] Directory '% s' created" % self.directory + terminalColors.ENDC)
        except OSError:
            print(terminalColors.FAIL + OSError + terminalColors.ENDC)

def help():
    print(terminalColors.INFO + """ 
PRINTS THIS HELP MENU

USAGE: python3 initHTB.py -i <IP> -d <VHOST>
    -i <IP> : IP of the VHOST
    -d <VHOST> : VHOST NAME
    -h : Prints this help menu
    -I : Initialize the initHTB.py script 
         Creates a directory for HTB if it doesn't exist, as per default configurations.
         To change the configurations, edit the config.json file    
    """ + terminalColors.ENDC)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        help()
        sys.exit(1)
    elif len(sys.argv) == 2:
        with open('config.json') as json_file:
            config = json.load(json_file)

        if sys.argv[1] == '-h':
            help()
            sys.exit(1)
        elif sys.argv[1] == '-I':
            print("REACHED IF CONDITION")
            initHTB(config).create_directory()
            sys.exit(1)
        elif sys.argv[1] == '-i':
            print(terminalColors.FAIL + "[-] Please provide the VHOST use -d flag" + terminalColors.ENDC)
            sys.exit(1)
        elif sys.argv[1] == '-d':
            print(terminalColors.FAIL + "[-] Please provide the IP use -i flag" + terminalColors.ENDC)
            sys.exit(1)
        elif sys.argv[1] == '-i' and sys.argv[3] == '-d':
            with open('config.json') as json_file:
                config = json.load(json_file)
            initHTB(config).initialize()
            sys.exit(1)
        else:
            print(terminalColors.FAIL + "[-] Invalid argument" + terminalColors.ENDC)
            help()
            sys.exit(1)


        
