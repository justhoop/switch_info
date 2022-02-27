from ast import arg
from netmiko import ConnectHandler
from getpass import getpass, getuser
from sys import argv
from os import system

def testping(host):
    response = system('ping -n 2 ' + host)
    if response == 0:
        return True
    else:
        return False

def processcommand(cisco1, command):
    with ConnectHandler(**cisco1) as net_connect:
        output = net_connect.send_command(command)
    return output

def assignarguments(args):
    if len(args) == 1:
        host = input('host: ')
        user = input('user: ')
        mac = input('mac: ')
    elif len(args) == 3:
        host = args[1]
        mac = args[2]
        user = getuser()
    elif len(args) == 4:
        host = args[1]
        user = args[2]
        mac = args[3]
    else:
        print('not enough arguments to work with')
        exit
    return host, user, mac

host, user, mac = assignarguments(argv)

if testping(host):
    print(user)
    cisco1 = { 
        "device_type": "cisco_ios",
        "host": host,
        "username": user,
        "password": getpass(),
    }
    port = processcommand(cisco1, f"show mac address-table | inc {mac}")
    if port:
        print(port)
    else:
        print(f"{mac} not found")
else:
    print("host not responding")