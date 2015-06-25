from node import *
from labelmaker import *

class assembler(object):

    def __init__(self):
        self.instructions = []
        self.binops =  {'+' : 'add',
                        '-' : 'sub',
                        '/' : 'div',
                        '*' : 'mul' }
        self.conds = {'==' : 'je',
                      '!=' : 'jne',
                      '>' : 'jg',
                      '<' : 'jl' }
        self.labelmaker = labelmaker()

    def write_to_file(self, sourceFilename, targetFilename):
        with open(targetFilename, 'w') as f:
            f.write(";\n; ASSEMBLY OUTPUT FOR: " + sourceFilename + "\n")
            f.write(";\n; Generated by TINY->ASM compiler\n")
            f.write(";\n; Author David Sverdlov\n")
            for instr in self.instructions:
                f.write(instr + "\n")

    def add(self, instruction):
        self.instructions.append(instruction)

    def assemble(self, tree):
        def mov(reg, constant):
            self.add("\t mov \t " + reg + ", " + str(constant) + "\t\t ; Store constant " +str(constant) + "in the acc")
        def var_store(var, val):
            self.add("\t mov \t byte ptr ["+var+"], "+str(val)+" \t\t ; Store the value "+str(val)+" into the byte at location "+var)
        def var_stack(var):
            self.add("\t push \t "+var+" \t\t ; Push the 4 bytes at address var to the stack")

        def offset_locals(variables):
                self.add(" ; Offsets for local variables ")
                i = 0
                for var in variables:
                    i -= 4
                    self.add("\t .equ \t " + str(var.children[1]) + " " + str(i) + "\t\t ; " + str(var.children[0]) + " " + str(var.children[1]))
                if(i < 0):
                    self.add("\t sub \t ESP, " + str(-i) + "\t\t ; Adjust stack pointer to reserve space")

        def process_params(tree):
            for par in tree.children:
                self.add("\t push \t " + str(par) + " \t\t ; Push parameter " + str(par) + " on stack")

        def process_math(tree):
            op = self.binops.get(tree.data)
            #If we execute the code to place the left operand in the accumulator register,
            # and then execute the code to place the right operand in the accumulator register,
            # we will overwrite the value of the left operand with the value of the right operand
            mov('EAX', tree.children[1]) # right operand!
            self.add("\t push \t EAX \t\t ; Push *right* operand on the stack")
            mov('EAX', tree.children[0]) # left # TODO what if nodes
            self.add("\t pop \t EBX \t\t ; Pop the *right* operand from the stack")
            self.add("\t " + op + " \t EAX, EBX \t\t ; Do the " + op + ", store result on the stack")

        def process_function_call(tree):
            self.assemble(tree.children[1:]) # params
            self.add( "\t call \t " + tree.children[0] + " \t\t ; Make the function call")
            self.add( "\t add \t ESP, " + str(len(tree.children[1:]) * 4) + " \t\t ; Pop the input params")
            self.add( "\t push \t EAX \t\t ; Push the result on the stack ")

        def process_condition(tree):
            cond = self.conds.get(tree.data)
            for child in tree.children:
                self.assemble(child)
            self.add("\t pop \t EAX \t\t ; Pop the second operand to the accumulator")
            self.add( "\t cmp \t [ESP], EAX \t\t ; Compare 1st operand (stack) to accmltr")
            #self.add( "\t cmp \t [ESP], EAX \t\t ")
            self.add( "\t setg \t [ESP] \t\t ; Place proper boolean value on stack")

        def process_if_then(tree):
            # needs to jump over then clause child[2] so we need a label
            endlabel = self.labelmaker.getLabel()
            self.assemble(tree.children[0]) # cond
            self.add( "\t pop \t EAX \t\t ; Pop value on the top of stack")
            self.add( "\t cmp \t EAX, 0 \t\t ; Compare expr with 0")
            self.add( "\t jne \t " + endlabel + " \t\t ; Jump if popped value is not false")
            self.assemble(tree.children[1]) # then
            self.add( endlabel + ": \t\t ; End if-then structure")

        def process_if_then_else(tree):
            endlabel = self.labelmaker.getLabel() # "endif2"
            elselabel = self.labelmaker.getLabel() # "else2"
            self.assemble(tree.children[0]) #cond
            self.add( "\t pop \t EAX \t\t ; Pop value on top of stack")
            self.add( "\t cmp \t EAX, 0 \t\t ; Compare expr with 0")
            self.add( "\t je \t " + elselabel + " \t\t ; Jump if popped value is false")
            self.assemble(tree.children[1]) # then code
            self.add( "\t jmp \t " + endlabel + " \t\t ; Jump over else clause to end")
            self.add( elselabel + ": \t\t ; Begin Else code")
            self.assemble(tree.children[2]) # else code
            self.add( endlabel + ": \t\t ; End if-then-else structure")

        def process_while(tree):
            condlabel = self.labelmaker.getLabel() #"condlabel"
            endlabel = self.labelmaker.getLabel() #"endwhile"
            self.add( condlabel + ": \t\t ; Begin condition of while")
            self.assemble(tree.children[0])
            self.add( "\t cmp \t EAX, 0 \t\t ; Compare cond res with 0")
            self.add( "\t je \t "+ endlabel + " \t\t ; End the while if false")
            self.assemble(tree.children[1])
            self.add( "\t jmp \t " + condlabel + " \t\t ; Jump back to condition")
            self.add( endlabel + ": \t\t ; End while structure")

        def process_return(tree):
            self.assemble(tree.children[0])
            self.add( "\t ret \t \t\t ; Return after pushing things on the stack")

        def process_block(tree):
            variables = tree.children[0].children
            statements = tree.children[1].children

            offset_locals(variables)
            for s in statements:
                self.assemble(s)

        def process_function_declaration(tree):
            description =  "; Function declaration: " + tree.children[0] + " " + tree.children[1] + "("
            bodyNode = tree.children[2]
            if(len(tree.children) == 4): # if there are formal params
                bodyNode = tree.children[3]
                for fpar in tree.children[2].children:
                    description += fpar.children[0] + " " + fpar.children[1] + ", "
                description = description.rstrip(", ") # remove last comma
            description += ")"
            self.add( description )

            self.add( ".globl " + tree.children[1] )
            self.add( ".type " + tree.children[1] + ", @function" )
            self.add( tree.children[1] + ":" )
            self.add( "\t push \t EBP \t\t ; Save base ptr on stack" )
            self.add( "\t mov \t EBP, ESP \t\t ; Base ptr is stack ptr" )

            # offset for params

            if(len(tree.children) == 4):
                self.add( "; Calculate offsets for formal parameters" )
                first = 8
                for fpar in reversed(tree.children[2].children):
                    self.add( "\t .equ \t " + fpar.children[1] + " " + str(first) + "\t\t ; " + fpar.toString() )
                    first += 4

            self.add( "; Locals NYI" )
            self.add( "; Body of: " + tree.children[1] )
            self.assemble(bodyNode)

            # aftermath
            self.add( "; Cleaning up: " + tree.children[1] )
            self.add( "ENDLABEL: " )
            self.add( "\t mov \t ESP, EBP \t\t ; Restore stack pointer" )
            self.add( "\t pop \t EBP \t\t ; Restore base ptr" )
            self.add( "\t ret " )

            self.add( " ;;;;; " )
        # End of function declaration

        def process_assignment_array(tree):
            node = tree.children[0]
            # probably an array assign x[i] = n
            self.add( " ; " + node.children[0] + "[" + node.children[1] + "] = " + tree.children[1] )
            self.add( "\t mov \t EAX, (EBP)*" + str(node.children[0]) + " \t\t ; " )
            self.add( "\t add \t EAX, " + str(node.children[1]) )
            self.add( "\t mov \t (EAX), " + str(tree.children[1]) )

        def process_assignment(tree):
            if type(tree.children[1]) is Node:
                # if assingning value is a node, assemble that first
                self.assemble(tree.children[1])

            self.add( "\t mov \t [EBP+" + tree.children[0] + "], " + str(tree.children[1]) + "\t\t ; " + tree.children[0] + " = " + str(tree.children[1]) )


        def process_write(tree):
            self.assemble(tree.children[0])
            self.add( "\t mov \t EDX, " + "messagelength" + " \t\t ; Write message length to EDX")
            self.add( "\t mov \t ECX, " + "messagevar" + "\t\t ; Message to write")
            self.add( "\t mov \t EBX, 1 \t\t ; File descriptor (stdout)")
            self.add( "\t mov \t EAX, 4 \t\t ; System call number (sys_write)")
            self.add( "\t int \t 0x80 \t\t ; Call kernel")


        def process_program(tree):
            #self.add(".model small \n .stack 4096 \n .data  \n.code \n main:")
            self.add(";")
            self.add(".globl _start")
            self.add(".type _start, @function")
            self.add("_start:")
            self.add("\t call \t main")
            self.add("\t mov \t EBX, 0")
            self.add("\t mov \t EAX, 1")
            self.add("\t int \t 0x80")
            for child in tree.children:
                self.assemble(child)


        if type(tree) != Node:
            self.add("\t push \t " + str(tree) + "\t\t ; Push " + str(tree) + " on the stack")

        elif tree.data == 'params':
            process_params(tree)

        elif tree.data == 'declaration' or tree.data == 'program': # todo fix root
            process_program(tree)

        elif self.binops.has_key(tree.data):
            process_math(tree)

        elif self.conds.has_key(tree.data):
            process_condition(tree)

        elif tree.data == 'fCall':
            process_function_call(tree)

        elif tree.data == 'if' and len(tree.children) == 2:
            process_if_then(tree)

        elif tree.data == 'if' and len(tree.children) == 3:
            process_if_then_else(tree)

        elif tree.data == 'while':
            process_while(tree)

        elif tree.data == 'return':
            process_return(tree)

        elif tree.data == 'block':
            process_block(tree)

        elif tree.data == 'write':
            process_write(tree)

        elif tree.data == 'FUNCTION':
            process_function_declaration(tree)

        elif tree.data == 'assign' and type(tree.children[0]) is Node:
            process_assignment_array(tree)

        elif tree.data == 'assign': # if we get here, the value is not another node
            process_assignment(tree)



        else:
            for child in tree.children:
                self.assemble(child)