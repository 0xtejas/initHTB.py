#!/usr/bin/env python3

import os
import subprocess
import json

# TERMINAL COLORS - CODE FROM https://stackoverflow.com/a/287944/11561065
class terminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
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
            print(terminalColors.OKGREEN + "[+] Directory '% s' created" % self.directory + terminalColors.ENDC)

        except OSError:
            print(terminalColors.FAIL + "[-] Directory '% s' already exists" % self.directory + terminalColors.ENDC)
    

        with open('/etc/hosts','r') as file:
            content = file.read()

            new_content = content.replace("\n\n",f"\n{self.ip}    {self.directory.lower()}.htb\n\n",1)
        try:
            with open('/etc/hosts','w') as file:
                file.write(new_content)

            print(terminalColors.OKGREEN + f"[+] IP: {self.ip} and HOST: {self.directory.lower()}.htb is added to the file!" + terminalColors.ENDC)
        except:
            print(terminalColors.FAIL + "[-] Error while writing to file" + terminalColors.ENDC)
            print(terminalColors.FAIL + "[-] Please check the file permissions" + terminalColors.ENDC)

if __name__ == "__main__":
    with open('config.json','r') as f:
        object = initHTB(json.load(f))
        object.initialize()

        
