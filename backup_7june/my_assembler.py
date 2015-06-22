from node import *


class assembler(object):

    def __init__(self):
        self.instructions = []

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
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
            
        if(type(tree) != Node):
            self.add("\t push \t " + str(tree) + "\t\t ; Push " + str(tree) + " on the stack")

        elif(tree.data == 'params'):
            for par in tree.children:
                self.add("\t push \t " + str(par) + " \t\t ; Push parameter " + str(par) + " on stack")
            
        elif(tree.data == 'declaration' or tree.data == 'program'): # todo fix root
            self.add("; ASSEMBLY OUTPUT FOR " + "[TODO INSERT FILENAME]")
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

        elif(tree.data == '+'):
            #If we execute the code to place the left operand in the accumulator register,
            # and then execute the code to place the right operand in the accumulator register,
            # we will overwrite the value of the left operand with the value of the right operand
            mov('EAX', tree.children[1]) # right operand!
            self.add("\t push \t EAX \t\t ; Push *right* operand on the stack")
            mov('EAX', tree.children[0]) # left # TODO what if nodes
            self.add("\t pop \t EBX \t\t ; Pop the *right* operand from the stack")
            self.add("\t add \t EAX, EBX \t\t ; Do the addition, store result on the stack")

        elif(tree.data == '-'):
            for child in tree.children:
                self.assemble(child)
            self.add("\t pop \t EAX \t\t ; Pop the first argument of the stack into the accumulator")
            self.add("\t sub \t [ESP], EAX \t\t ; Do the subtraction, store result on the stack")

        elif(tree.data == '*'):
            for child in tree.children:
                self.assemble(child)
            self.add("\t pop \t EAX \t\t ; Pop the first argument of the stack into the accumulator")
            self.add("\t mul \t [ESP], EAX \t\t ; Do the multiplication, store result on the stack")

        elif(tree.data == '/'):    
            for child in tree.children:
                self.assemble(child)
            self.add("\t pop \t EAX \t\t ; Pop the first argument of the stack into the accumulator")
            self.add( "\t div \t [ESP], EAX \t\t ; Do the division, store result on the stack")

        elif(tree.data == '>'):
            for child in tree.children:
                self.assemble(child)
            self.add("\t pop \t EAX \t\t ; Pop the second operand to the accumulator")
            self.add( "\t cmp \t [ESP], EAX \t\t ; Compare 1st operand (stack) to accmltr")
            #self.add( "\t cmp \t [ESP], EAX \t\t ")
            self.add( "\t setg \t [ESP] \t\t ; Place proper boolean value on stack")

        elif(tree.data == '=='):
            for child in tree.children:
                self.assemble(child)
            self.add( "\t pop \t EAX \t\t ; Pop the second operand to the accumulator")
            self.add( "\t cmp \t [ESP], EAX \t\t ; Compare 1st operand (stack) to accmltr")
            self.add( "\t cmp \t == \t\t ; TODO")
            #self.add( "\t setg \t [ESP] \t\t ; Place proper boolean value on stack")

        elif(tree.data == '!='):
            for child in tree.children:
                self.assemble(child)
            self.add( "\t pop \t EAX \t\t ; Pop the second operand to the accumulator")
            self.add( "\t cmp \t [ESP], EAX \t\t ; Compare 1st operand (stack) to accmltr")
            self.add( "\t != \t [ESP], EAX \t\t ; TODO")
            #self.add( "\t setg \t [ESP] \t\t ; Place proper boolean value on stack")

        elif(tree.data == 'fCall'):
            self.assemble(tree.children[1]) # params
            self.add( "\t call \t " + tree.children[0] + " \t\t ; Make the function call")
            self.add( "\t add \t ESP, " + str(len(tree.children[1]) * 4) + " \t\t ; Pop the input params")
            self.add( "\t push \t EAX \t\t ; Push the result on the stack ")
            
        elif(tree.data == 'if' and len(tree.children) == 2):
            # needs to jump over then clause child[2] so we need a label
            endlabel = "endif" # generate labels?
            self.assemble(tree.children[0]) # cond
            self.add( "\t pop \t EAX \t\t ; Pop value on the top of stack")
            self.add( "\t cmp \t EAX, 0 \t\t ; Compare expr with 0")
            self.add( "\t jne \t " + endlabel + " \t\t ; Jump if popped value is not false")
            self.assemble(tree.children[1]) # then
            self.add( endlabel + ": ")
            
        elif(tree.data == 'if' and len(tree.children) == 3):
            endlabel = "endif2" # todo gen
            elselabel = "else2" # todo gen
            self.assemble(tree.children[0]) #cond
            self.add( "\t pop \t EAX \t\t ; Pop value on top of stack")
            self.add( "\t cmp \t EAX, 0 \t\t ; Compare expr with 0")
            self.add( "\t je \t " + elselabel + " \t\t ; Jump if popped value is false")
            self.assemble(tree.children[1]) # then code
            self.add( "\t jmp \t " + endlabel + " \t\t ; Jump over else clause to end")
            self.add( elselabel + ": ")
            self.assemble(tree.children[2]) # else code
            self.add( endlabel + ": ")
            
        elif(tree.data == 'while'):
            condlabel = "condlabel"
            endlabel = "endwhile"
            self.add( condlabel + ": ")
            self.assemble(tree.children[0])
            self.add( "\t cmp \t EAX, 0 \t\t ; Compare cond res with 0")
            self.add( "\t je \t "+ endlabel + " \t\t ; End the while if false")
            self.assemble(tree.children[1])
            self.add( "\t jmp \t " + condlabel + " \t\t ; Jump back to condition")
            self.add( endlabel + ": ")
            
        elif(tree.data == 'return'):
            self.assemble(tree.children[0])
            self.add( "\t ret \t \t\t ; Return")

        elif(tree.data == 'block'):
            variables = tree.children[0].children
            statements = tree.children[1].children

            offset_locals(variables)
            for s in statements:
                self.assemble(s)
            
        elif(tree.data == 'write'):
            self.assemble(tree.children[0])
            self.add( "\t mov \t EDX, " + "messagelength" + " \t\t ; Write message length to EDX")
            self.add( "\t mov \t ECX, " + "messagevar" + "\t\t ; Message to write")
            self.add( "\t mov \t EBX, 1 \t\t ; File descriptor (stdout)")
            self.add( "\t mov \t EAX, 4 \t\t ; System call number (sys_write)")
            self.add( "\t int \t 0x80 \t\t ; Call kernel")

        elif(tree.data == 'FUNCTION'):
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

        elif(tree.data == 'assign') and type(tree.children[0]) is Node:
            node = tree.children[0]
            # probably an array assign x[i] = n
            self.add( " ; " + node.children[0] + "[" + node.children[1] + "] = " + tree.children[1] )
            self.add( "\t mov \t EAX, (EBP)*" + str(node.children[0]) + " \t\t ; " )
            self.add( "\t add \t EAX, " + str(node.children[1]) )
            self.add( "\t mov \t (EAX), " + str(tree.children[1]) )

        elif tree.data == 'assign': # if we get here, the value is not another node
            if type(tree.children[1]) is Node:
                # if assingning value is a node, assemble that first
                self.assemble(tree.children[1])
               
            self.add( "\t mov \t [EBP+" + tree.children[0] + "], " + str(tree.children[1]) + "\t\t ; " + tree.children[0] + " = " + str(tree.children[1]) )
            
        else:
            for child in tree.children:
                self.assemble(child)
