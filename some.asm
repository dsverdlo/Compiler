
section	.text
	global _start       ;must be declared for using gcc
_start:                     ;tell linker entry point
	 push 	 3		 ; Push 1 on the stack
	 push 	 2		 ; Push 2 on the stack
	 pop 	 EAX 		 ; Pop the second operand to the accumulator
	 cmp 	 [ESP], EAX 		 ; Compare 1st operand (stack) to accmltr
	 setg 	 [ESP] 		 ; Place proper boolean value on stack
	 pop 	 EAX 		 ; Pop value on top of stack
	 cmp 	 EAX, 0 		 ; Compare expr with 0
	 je 	 else2 		 ; Jump if popped value is false
			 ; Push 1 on the stack
	 
	mov	edx, len1    ;message length
	mov	ecx, msg1    ;message to write
	mov	ebx, 1	    ;file descriptor (stdout)
	mov	eax, 4	    ;system call number (sys_write)
	int	0x80        ;call kernel
	
	 jmp 	 endif2 		 ; Jump over else clause to end
else2: 
	 		 ; Push 2 on the stack
	 
	mov	edx, len2    ;message length
	mov	ecx, msg2    ;message to write
	mov	ebx, 1	    ;file descriptor (stdout)
	mov	eax, 4	    ;system call number (sys_write)
	int	0x80        ;call kernel
	  	 		 ; Return
endif2: 

	mov	edx, len     ;message length
	mov	ecx, msg    ;message to write
	mov	ebx, 1	    ;file descriptor (stdout)
	mov	eax, 4	    ;system call number (sys_write)
	int	0x80        ;call kernel
	mov	eax, 1	    ;system call number (sys_exit)
	int	0x80        ;call kernel

section .data

msg  	db	'derp, world!',0xa	;our dear string
len	    equ	$ - msg			;length of our dear string
msg1	db	'Message1, world!',0xa	;our dear string
len1	equ	$ - msg1			;length of our dear string
msg2	db	'Message2, world!',0xa	;our dear string
len2	equ	$ - msg2			;length of our dear string
