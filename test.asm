;
; ASSEMBLY OUTPUT FOR: test.tiny
;
; Generated by TINY->ASM compiler
;
; Author David Sverdlov
;
.globl _start
.type _start, @function
_start:
	 call 	 main
	 mov 	 EBX, 0
	 mov 	 EAX, 1
	 int 	 0x80
; Function declaration: int gggg(int y)
.globl gggg
.type gggg, @function
gggg:
	 push 	 EBP 		 ; Save base ptr on stack
	 mov 	 EBP, ESP 		 ; Base ptr is stack ptr
; Calculate offsets for formal parameters
	 .equ 	 y 8		 ; (fparam: int, y)
; Locals NYI
; Body of: gggg
 ; Offsets for local variables 
	 push 	 5		 ; Push 5 on the stack
	 mov 	 EDX, messagelength 		 ; Write message length to EDX
	 mov 	 ECX, messagevar		 ; Message to write
	 mov 	 EBX, 1 		 ; File descriptor (stdout)
	 mov 	 EAX, 4 		 ; System call number (sys_write)
	 int 	 0x80 		 ; Call kernel
; Cleaning up: gggg
ENDLABEL: 
	 mov 	 ESP, EBP 		 ; Restore stack pointer
	 pop 	 EBP 		 ; Restore base ptr
	 ret 
 ;;;;; 
