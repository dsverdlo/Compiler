; ASSEMBLY OUTPUT FOR [TODO INSERT FILENAME]
;
.globl _start
.type _start, @function
_start:
	 call 	 main
	 mov 	 EBX, 0
	 mov 	 EAX, 1
	 int 	 0x80
; Function declaration: int main()
.globl main
.type main, @function
main:
	 push 	 EBP 		 ; Save base ptr on stack
	 mov 	 EBP, ESP 		 ; Base ptr is stack ptr
; Calculate offsets for formal parameters
; Locals NYI
; Body of: main
 ; Offsets for local variables 
	 push 	 1		 ; Push 1 on the stack
	 mov 	 EDX, messagelength 		 ; Write message length to EDX
	 mov 	 ECX, messagevar		 ; Message to write
	 mov 	 EBX, 1 		 ; File descriptor (stdout)
	 mov 	 EAX, 4 		 ; System call number (sys_write)
	 int 	 0x80 		 ; Call kernel
	 push 	 1		 ; Push 1 on the stack
	 ret 	 		 ; Return
; Cleaning up: main
ENDLABEL: 
	 mov 	 ESP, EBP 		 ; Restore stack pointer
	 pop 	 EBP 		 ; Restore base ptr
	 ret 
 ;;;;; 
