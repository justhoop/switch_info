from netmiko import ConnectHandler
from os import system
from os import getenv
import socket

def testconnection(host):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	response = sock.connect_ex((host, 22))
	if response == 0:
		return True
	else:
		return False

def processcommand(cisco1, command):
    with ConnectHandler(**cisco1) as net_connect:
        output = net_connect.send_command(command)
    return output

def unusedports(ports):
	interfaces = "Name,LastInput,LastOutPut\n"
	for line in ports:
		if line[0] != ' ' and 'Vlan' not in line and 'is down' in line:
			interface = line.split(" ")[0]
		elif 'Last input' in line:
			if 'interface' in locals():
				interface += ',' + line.split(",")[0].strip().split(" ")[-1]
				interface += ',' + line.split(",")[1].strip().split(" ")[-1] + "\n"
				interfaces += interface
				del interface
	return interfaces

def getunusedports(host):
	user = getenv('SWITCH_USER','none')
	password = getenv('SWITCH_PW','none')
	if(user == 'none' or password == 'none'):
		print(f"No environment variables")
		exit()
	if testconnection(host):
		cisco1 = {
			"device_type": "cisco_ios",
			"host": host,
			"username": user,
			"password": password,
		}
		hostname = (processcommand(
			cisco1, "show running-config | include hostname")).split(' ')[1] + '.csv'
		print(f"Processing {hostname}")
		# unusedPorts = processcommand(
			# cisco1, "show interfaces | include proto.*notconnect|proto.*administratively down|Last in.*[1-9][4-9]w[0-9]|[0-9]y|disabled|Last input never, output never, output hang never")
		ports = processcommand(cisco1, "show interfaces")
		unused = getunusedports(ports)
		with open(hostname, 'w') as f:
			f.write(unused)
	else:
		print(f"{host} is not reachable")

with open('switches.txt', 'r') as f:
	hosts = f.readlines()
for host in hosts:
	host = host.replace("\n","")
	getunusedports(host)
