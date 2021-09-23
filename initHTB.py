#!/usr/bin/env python3

import os
import subprocess
import json





with open('config.json', 'r') as f:
    config = json.load(f)
    parent_dir = config['parent_directory'].replace('\"$USER\"', os.environ['USER'])
    


directory=input("Enter the Machine Name: ")
ip=input("Enter the IP: ")

path = os.path.join(parent_dir,directory)
os.mkdir(path)
print("[+] Directory '% s' created" % directory)

print("[+] Adding host to host file")

with open('/etc/hosts','r') as file:
    content = file.read()


new_content = content.replace("\n\n",f"\n{ip}    {directory.lower()}.htb\n\n",1)

with open('/etc/hosts','w') as file:
    file.write(new_content)

print(f"[+] IP:{ip} and HOST:{directory.lower()}.htb is added to the file!")








