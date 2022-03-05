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

    print(output)

if len(argv) == 2:
    host = argv[1]
    user = getuser()
elif len(argv) == 3:
    host = argv[1]
    user = argv[2]
else:
    host = input('host: ')
    user = input('user: ')
if not user:
    user = getuser()

if testping(host):
    print(user)
    cisco1 = { 
        "device_type": "cisco_ios",
        "host": host,
        "username": user,
        "password": getpass(),
    }
    # processcommand(cisco1, "show conf")
    processcommand(cisco1, "show version")
else:
    print("host not responding")