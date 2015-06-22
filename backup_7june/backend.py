# back end, optimizing and code gen
#
# http://en.wikipedia.org/wiki/Global_value_numbering
#
#
#
#
from node import *

def optimise(ast):
    #optimise_common_subexpression(ast)
    optimise_dead_code(ast)
    optimise_constant_fold(ast)

    return ast

# CSE refers to evaluating duplicate subexpressions only once
def optimise_common_subexpression(ast):
    pass

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

# right now only detects code after a return statement
def optimise_dead_code(ast):
    dead_code = []
    if((type(ast) == type("")) or (type(ast) == type(1)) or ast.is_empty()):
        #print "Dropping ", ast
        return dead_code
    else:
        return_found = False
        for child in ast.children:
            if((type(child) == type(ast)) and
               (child.data == 'return') and
               not(return_found)):
                return_found = True
            else:
                if return_found: # return already appeared son
                    dead_code.append(child)
                    print "\nDeleting/ dead code: ", child.toString()
                    ast.children.remove(child)
                
            opt_child = optimise_dead_code(child)
            if(opt_child != []):
                dead_code.append(opt_child)
            
                
    return flatten(dead_code)


# Constant folding is the process of recognizing and evaluating
# constant expressions at compile time rather than computing them at runtime.
def optimise_constant_fold(root, part = None):

    def replace_node(node, value):
        print "Folding node: " + node.toString() + " by " + str(value)
        i = node.parent.children.index(node)
        node.parent.children.remove(node)
        node.parent.children.insert(i, value)

    def children_ints(node):
        for child in node.children:
            if not(type(child) is int):
                return False
        return True
    
    def recursive_place(ast, ignore, var, value, stopnode):
        print "Searching for ["+str(var)+"] to ["+str(value)+"] in tree: " + str(ast)
        if (type(ast) == Node and not(stopnode.data)):
            print "-- node received: " + str(ast.data)
            if ast.data == var:
                ast.data = value # leaf node
                print "LEAF NODE SWITCHED"
            else:
                # data is another node
                1+2
            
            for child in ast.children:
                print "--- recurception: " + str(child)

                if(ignore in ast.children and
                   (ast.children.index(child) <= ast.children.index(ignore))):
                    print "--- skipping previous nodes"
                    continue

                if(ast.data == 'assign' and child == var):
                    print "--- NEW ASSIGNMENT FOUND. STOP REPLACING ["+str(var)+"] by ["+str(value)+"]"
                    stopnode.data = True # stop mechanism
                    return
                    
                # if a child is the var, and we are not in an assign, replace it
                if(child == var):
                    i = ast.children.index(child)
                    ast.children.remove(child)
                    ast.children.insert(i, value)
                    print "X REPLACED -- new node: " + str(ast)
                else:
                    # else we need to go deeper into nodes
                    if(type(child) == Node):
                        recursive_place(child, ignore, var, value, stopnode)
            # replace binary instructions
            if ast.data == '/' and children_ints(ast):
                replace_node(ast, ast.children[0] / ast.children[1])
            elif ast.data == '*' and children_ints(ast):
                replace_node(ast, ast.children[0] * ast.children[1])
            elif ast.data == '+' and children_ints(ast):
                replace_node(ast, ast.children[0] + ast.children[1])
            elif ast.data == '-' and children_ints(ast):
                replace_node(ast, ast.children[0] - ast.children[1])
                
                                                      
                                
                                                      
        
            
                
        

    if(part is None):
        part = root
        
    if(type(part) == Node):
        if (part.data == 'assign') and len(part.children) >= 2:
            var = part.children[0]
            print "got one: " + str(var)
            if(type(part.children[1]) == int or type(part.children[1]) == str):
                value = part.children[1]
                print "continue: " + str(value)
                recursive_place(root, part, var, value, Node(False))
        
            #if(type(ast.children[1]) == Node and ast.children[1].data
        else:
            for child in part.children:
                optimise_constant_fold(part, child)
    else:
        print ""


def flatten_instructions(tree, lblmkr):
    
    def insert_before_statement(tree, node):
        if not(type(tree.parent) is Node): return
        print "\ins " + tree.toString()
        if(tree.parent.data == 'STATEMENTS'):
            pos = tree.parent.children.index(tree)
            tree.parent.children.insert(pos, node)
            node.parent = tree.parent
            print "Done: ", tree.parent
        else:
            insert_before_statement(tree.parent, node)

    def add_to_declarations(tree, node):
        if not(type(tree) is Node): return
        if(tree.data == 'block'):
            tree.children[0].add_child(node)
            print "BLOCK: ", tree
        else:
            add_to_declarations(tree.parent, node)

    def do_flattening(node):
        if not(type(tree) is Node): return

        grabparent = node.parent
        print " ; Flattening node: " + str(node) + " of: " + str(node.parent)

        tmpvar = lblmkr.getTempVar()

        decl = Node('var')
        decl.add_child('int') # char??
        decl.add_child(tmpvar)
        add_to_declarations(node, decl)
        #print "--", decl.parent

            
        assign = Node('assign')
        assign.add_child(tmpvar)
        #assign.add_child('placeholder')
        assign.add_child(node)
        
        x = grabparent
        while type(x) is Node:
            #print " # " + x.data
            x = x.parent
        
        insert_before_statement(grabparent, assign) # TODO remove one iteration?
        #print "--", assign.parent
                        
        i = grabparent.children.index(node)
        grabparent.children.remove(node) # remove child
        grabparent.children.insert(i, tmpvar) # insert tmp var


        
    def flatten_statement(tree): # tree is a statement at first

        if not(type(tree) is Node): return tree

        if tree.data == 'assign':
            for child in tree.children:
                flatten_statement(child)
            return tree
            
        if tree.data in ['if', 'while']:
            for block in tree.children[1:]: # ignore first child (condition)
                for stmt in block.children[1].children: # [1] is statements
                    #print "** Found a nested stmt: ", stmt
                    flatten_statement(stmt)
            return tree

        # Otherwise we can probably substitute some parts
        for child in tree.children:
            if(type(child) is Node): # foreach child that is a node                       
                #print "--", child   
                do_flattening(child)                        
                #print "--", child        
                flatten_statement(child) # iterate to go deeper
        return tree
            

    if(type(tree) is Node):
        if(tree.data == 'STATEMENTS'):
            for statement in tree.children:
                #print "** Found a statement; ", statement
                flatten_statement(statement)
                return tree # done, no more iterating
        else:
            for child in tree.children:
                flatten_instructions(child, lblmkr) # iterate deeper until stmts or leaves found
        return tree
    else:
        return tree# leaf node, do nothing
    
    

class labelmaker(object):
    def __init__(self, fname = ""):
        self.n = 0
        self.fname = fname

    def getLabel(self):
        self.n += 1
        return "L" + str(self.n) + "_" + str(fname)

    def getTempVar(self):
        self.n += 1
        return "_tmp_" + str(self.n)

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
