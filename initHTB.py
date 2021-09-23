#!/usr/bin/env python3

import os
import subprocess
import json

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
            print("[+] Directory '% s' created" % self.directory)

        except OSError:
            print("[-] Directory '% s' already exists" % self.directory)
    

        with open('/etc/hosts','r') as file:
            content = file.read()

            new_content = content.replace("\n\n",f"\n{self.ip}    {self.directory.lower()}.htb\n\n",1)
        try:
            with open('/etc/hosts','w') as file:
                file.write(new_content)

            print(f"[+] IP: {self.ip} and HOST: {self.directory.lower()}.htb is added to the file!")
        except:
            print("[-] Error while writing to file")
            print("[-] Please check the file permissions")

if __name__ == "__main__":
    with open('config.json','r') as f:
        object = initHTB(json.load(f))
        object.initialize()

        
