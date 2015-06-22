from node import *

def assemble(tree):
    def mov(reg, constant):
        print "\t mov \t " + reg + ", " + str(constant) + "\t\t ; Store constant " +str(constant) + "in the acc"
    def var_store(var, val):
        print "\t mov \t byte ptr ["+var+"], "+str(val)+" \t\t ; Store the value "+str(val)+" into the byte at location "+var
    def var_stack(var):
        print "\t push \t "+var+" \t\t ; Push the 4 bytes at address var to the stack"

    def offset_locals(variables):
        print " ; Offsets for local variables "
        i = 0
        for var in variables:
            i -= 4
            print "\t .equ \t " + str(var.children[1]) + " " + str(i) + "\t\t ; " + str(var.children[0]) + " " + str(var.children[1])
        if(i < 0):
            print "\t sub \t ESP, " + str(-i) + "\t\t ; Adjust stack pointer to reserve space"
        
    if(type(tree) != Node):
        print "\t push \t " + str(tree) + "\t\t ; Push " + str(tree) + " on the stack"

    elif(tree.data == 'params'):
        for par in tree.children:
            print "\t push \t " + str(par) + " \t\t ; Push parameter " + str(par) + " on stack"
        
    elif(tree.data == 'declaration' or tree.data == 'program'): # todo fix root
        print "; ASSEMBLY OUTPUT FOR " + "[TODO INSERT FILENAME]" 
        #print ".model small \n .stack 4096 \n .data  \n.code \n main:"
        print ";"
        print ".globl _start"
        print ".type _start, @function"
        print "_start:"
        print "\t call \t main"
        print "\t mov \t EBX, 0"
        print "\t mov \t EAX, 1"
        print "\t int \t 0x80"
        for child in tree.children:
            assemble(child)

    elif(tree.data == '+'):
        #If we execute the code to place the left operand in the accumulator register,
        # and then execute the code to place the right operand in the accumulator register,
        # we will overwrite the value of the left operand with the value of the right operand
        mov('EAX', tree.children[1]) # right operand!
        print "\t push \t EAX \t\t ; Push *right* operand on the stack"
        mov('EAX', tree.children[0]) # left # TODO what if nodes
        print "\t pop \t EBX \t\t ; Pop the *right* operand from the stack"
        print "\t add \t EAX, EBX \t\t ; Do the addition, store result on the stack"

    elif(tree.data == '-'):
        for child in tree.children:
            assemble(child)
        print "\t pop \t EAX \t\t ; Pop the first argument of the stack into the accumulator"
        print "\t sub \t [ESP], EAX \t\t ; Do the subtraction, store result on the stack"

    elif(tree.data == '*'):
        for child in tree.children:
            assemble(child)
        print "\t pop \t EAX \t\t ; Pop the first argument of the stack into the accumulator"
        print "\t mul \t [ESP], EAX \t\t ; Do the multiplication, store result on the stack"

    elif(tree.data == '/'):    
        for child in tree.children:
            assemble(child)
        print "\t pop \t EAX \t\t ; Pop the first argument of the stack into the accumulator"
        print "\t div \t [ESP], EAX \t\t ; Do the division, store result on the stack"

    elif(tree.data == '>'):
        for child in tree.children:
            assemble(child)
        print "\t pop \t EAX \t\t ; Pop the second operand to the accumulator"
        print "\t cmp \t [ESP], EAX \t\t ; Compare 1st operand (stack) to accmltr"
        #print "\t cmp \t [ESP], EAX \t\t "
        print "\t setg \t [ESP] \t\t ; Place proper boolean value on stack"

    elif(tree.data == '=='):
        for child in tree.children:
            assemble(child)
        print "\t pop \t EAX \t\t ; Pop the second operand to the accumulator"
        print "\t cmp \t [ESP], EAX \t\t ; Compare 1st operand (stack) to accmltr"
        print "\t cmp \t == \t\t ; TODO"
        #print "\t setg \t [ESP] \t\t ; Place proper boolean value on stack"

    elif(tree.data == '!='):
        for child in tree.children:
            assemble(child)
        print "\t pop \t EAX \t\t ; Pop the second operand to the accumulator"
        print "\t cmp \t [ESP], EAX \t\t ; Compare 1st operand (stack) to accmltr"
        print "\t != \t [ESP], EAX \t\t ; TODO"
        #print "\t setg \t [ESP] \t\t ; Place proper boolean value on stack"

    elif(tree.data == 'fCall'):
        assemble(tree.children[1]) # params
        print "\t call \t " + tree.children[0] + " \t\t ; Make the function call"
        print "\t add \t ESP, " + str(len(tree.children[1]) * 4) + " \t\t ; Pop the input params"
        print "\t push \t EAX \t\t ; Push the result on the stack "
        
    elif(tree.data == 'if' and len(tree.children) == 2):
        # needs to jump over then clause child[2] so we need a label
        endlabel = "endif" # generate labels?
        assemble(tree.children[0]) # cond
        print "\t pop \t EAX \t\t ; Pop value on the top of stack"
        print "\t cmp \t EAX, 0 \t\t ; Compare expr with 0"
        print "\t jne \t " + endlabel + " \t\t ; Jump if popped value is not false"
        assemble(tree.children[1]) # then
        print endlabel + ": "
        
    elif(tree.data == 'if' and len(tree.children) == 3):
        endlabel = "endif2" # todo gen
        elselabel = "else2" # todo gen
        assemble(tree.children[0]) #cond
        print "\t pop \t EAX \t\t ; Pop value on top of stack"
        print "\t cmp \t EAX, 0 \t\t ; Compare expr with 0"
        print "\t je \t " + elselabel + " \t\t ; Jump if popped value is false"
        assemble(tree.children[1]) # then code
        print "\t jmp \t " + endlabel + " \t\t ; Jump over else clause to end"
        print elselabel + ": "
        assemble(tree.children[2]) # else code
        print endlabel + ": "
        
    elif(tree.data == 'while'):
        condlabel = "condlabel"
        endlabel = "endwhile"
        print condlabel + ": "
        assemble(tree.children[0])
        print "\t cmp \t EAX, 0 \t\t ; Compare cond res with 0"
        print "\t je \t "+ endlabel + " \t\t ; End the while if false"
        assemble(tree.children[1])
        print "\t jmp \t " + condlabel + " \t\t ; Jump back to condition"
        print endlabel + ": "
        
    elif(tree.data == 'return'):
        assemble(tree.children[0])
        print "\t ret \t \t\t ; Return"

    elif(tree.data == 'block'):
        variables = tree.children[0].children
        statements = tree.children[1].children

        offset_locals(variables)
        for s in statements:
            assemble(s)
        
    elif(tree.data == 'write'):
        assemble(tree.children[0])
        print "\t mov \t EDX, " + "messagelength" + " \t\t ; Write message length to EDX"
        print "\t mov \t ECX, " + "messagevar" + "\t\t ; Message to write"
        print "\t mov \t EBX, 1 \t\t ; File descriptor (stdout)"
        print "\t mov \t EAX, 4 \t\t ; System call number (sys_write)"
        print "\t int \t 0x80 \t\t ; Call kernel"

    elif(tree.data == 'FUNCTION'):
        description =  "; Function declaration: " + tree.children[0] + " " + tree.children[1] + "("
        bodyNode = tree.children[2]
        if(len(tree.children) == 4): # if there are formal params
            bodyNode = tree.children[3]
            for fpar in tree.children[2].children:
                description += fpar.children[0] + " " + fpar.children[1] + ", "
            description = description.rstrip(", ") # remove last comma
        description += ")"
        print description
        
        print ".globl " + tree.children[1]
        print ".type " + tree.children[1] + ", @function"
        print tree.children[1] + ":"
        print "\t push \t EBP \t\t ; Save base ptr on stack"
        print "\t mov \t EBP, ESP \t\t ; Base ptr is stack ptr"

        # offset for params

        if(len(tree.children) == 4):
            print "; Calculate offsets for formal parameters"
            first = 8
            for fpar in reversed(tree.children[2].children):
                print "\t .equ \t " + fpar.children[1] + " " + str(first) + "\t\t ; " + fpar.toString()
                first += 4

        print "; Locals NYI"
        print "; Body of: " + tree.children[1]
        assemble(bodyNode)
        
        # aftermath
        print "; Cleaning up: " + tree.children[1]
        print "ENDLABEL: "
        print "\t mov \t ESP, EBP \t\t ; Restore stack pointer"
        print "\t pop \t EBP \t\t ; Restore base ptr"
        print "\t ret "

        print " ;;;;; "

    elif(tree.data == 'assign') and type(tree.children[0]) is Node:
        node = tree.children[0]
        # probably an array assign x[i] = n
        print " ; " + node.children[0] + "[" + node.children[1] + "] = " + tree.children[1]
        print "\t mov \t EAX, (EBP)*" + str(node.children[0]) + " \t\t ; "
        print "\t add \t EAX, " + str(node.children[1])
        print "\t mov \t (EAX), " + str(tree.children[1])

    elif tree.data == 'assign': # if we get here, the value is not another node
        if type(tree.children[1]) is Node:
            # if assingning value is a node, assemble that first
            assemble(tree.children[1])
           
        print "\t mov \t [EBP+" + tree.children[0] + "], " + str(tree.children[1]) + "\t\t ; " + tree.children[0] + " = " + str(tree.children[1])
        
    else:
        for child in tree.children:
            assemble(child)
