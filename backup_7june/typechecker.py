#
# Type Checker functions
#
# We have to type check the following nodes:
#
# Assignment, function declarations, binary operations, Func calls, returns
from node import *

def type_check(node, errors):

    if not(type(node) is Node):
        return False

    if node.is_leaf():
        return find_type_of_leaf(node)

    if node.data == 'return':
        returnValue = node.children[0]
        returnType = find_type_of_var(returnValue, returnValue)
        fDecl = find_enclosing_fun(node)
        functionType = fDecl.children[0]
        if not returnType:
            print "Type check failed, no type found for variable: " + str(returnValue)
            return False

        if functionType == False:
            print "Type check failed, no type found for function " + fDecl.children[1]
            return False

        if returnType == functionType:
            return True

        print "Type check failed, returning [" + str(returnType) +"] when function '"+ fDecl.children[1] + "' should return [" + str(functionType) + "]"
        return False


    elif node.data == 'assignment':
        lexpType = find_type_of_var(node, node.children[0])
        rexpType = find_type_of_exp(node.children[1])
        if lexpType == rexpType:
            return True

        print "Type check failed, you tried assigning a [" + str(rexpType) + "] to variable " + str(node.children[0]) + " which has type [" + lexpType + "]"
        return False


    elif node.data == 'fCall':
        funDecl = find_fun_decl(node, node.children[0])
        if not funDecl:
            print "Type check failed, found no function with name: " + str(node.children[0])
            return False
        fparams = funDecl.children[2].children

        args = node.children[1:]

        if len(fparams) > len(args):
            print "Type check failed, too few arguments specified for function call to: " + str(node.children[0])
            return False
        if len(fparams) < len(args):
            print "Type check failed, too many arguments specified for function call to: " + str(node.children[0])
            return False

        for i in range(len(args)):
            argType = find_type_of_exp(args[i])
            fparamType = fparams[i].children[0]
            if not argType:
                print "Type check failed, no type found for argument ", args[i].toString()
                return False
            if argType != fparamType:
                print "Type check failed, function '" + node.children[0] + "' expected a [" + str(fparamType) + "] as argNo " + str(i+1) + ", but a [" + str(argType) + "] was given"

        return True

    elif node.data == 'fDecl':
        funReturnType = node.children[0]
        funName = node.children[1]
        funStatements = node.children[3].children[1] # block > statements
        for stmt in funStatements.children:
            if stmt.data == 'return':
                return type_check(stmt)
        # no return found yet, add our own
        if funReturnType == 'void':
            returnNode = Node('return')
            returnNode.add_child('void')
            funStatements.add_child(returnNode)
        else:
            print "Type check failed, no return statement found, while return type of "+funName+" is ["+funReturnType+"]"
            return False
        return True # we are good
    else:
        for c in node.children:
            type_check(c)
    return True







def find_fun_decl(tree, funname):
    if not(type(tree) is Node):
        return False
    if tree.data == 'program':
        for child in tree.children:
            if child.data == 'fDecl' and child.children[1] == funname:
                return child
    return find_fun_decl(tree.parent, funname)


def find_type_of_exp(tree):
    if not type(tree) is Node:
        return type_check(tree)

    if tree.is_leaf():
        return find_type_of_leaf(tree)

    if tree.data in ['+', '-', '*', '/', 'length']:
        lexpType = find_type_of_leaf(tree.children[0])
        rexpType = find_type_of_leaf(tree.children[1])

        # do potentional casting here
        if lexpType != 'int' or rexpType != 'int':
            print "Type check failed, '"+str(tree.data)+"' operation requires two integers, given: ["+ str(lexpType) +"] and ["+str(rexpType)+"]"
            return 'int'
        return 'int'

    if tree.data == 'fCall':
        return find_type_of_fun(tree.data, tree.children[0])

    if tree.data == 'array_access':
        return find_type_of_leaf(tree.children[0])

    if tree.data in ['or', 'and', 'not', '>', '>=', '<', '<=', '==', '!=']:
        return 'bool'



def find_type_of_leaf(leafnode):
    if leafnode.data == 'NUMBER':
        return 'int'
    elif leafnode.data == 'QCHAR':
        return 'char'
    elif leafnode.data == 'BOOL':
        return 'bool'
    elif leafnode.data == 'VAR':
        return find_type_of_var(leafnode.parent, leafnode.children[0])
    elif leafnode.data == 'array_access':
        return find_type_of_var(leafnode.parent, leafnode.children[0])
    else:
        return 'unknown'

def find_type_of_var(tree, varname):
    # if no varname specified, then it is <void>
    if varname == 'void':
        return varname

    # If not node then false
    if not(type(tree) is Node):
        return 'variable '+str(varname)+' not found'

    if tree.is_leaf():
        return find_type_of_leaf(tree)

    # if we reached a block, then check the variables
    if(tree.data == "block"):
        for variable in tree.children[0].children:
            if variable.children[1] == varname:
                return variable.children[0]
        # if not found, try higher
    # if we reached program node, check all children (varDecl)'s
    if tree.data == 'program':
        for decl in tree.children:
            if decl.data == 'varDecl' and decl.children[1] == varname:
                return decl.children[0]

    # if we reached a func declaration, check parameters
    if tree.data == 'fDecl':
        for fparam in tree.children[2].children:
            if fparam.data == 'fparam' and fparam.children[1] == varname:
                return fparam.children[0]

    # We have not reached a block yet, so go up
    return find_type_of_var(tree.parent, varname)


def find_enclosing_fun(tree):
    # If not node then false
    if not(type(tree) is Node):
        return False

    # if we reached the func declaration, return it
    if(tree.data == "fDecl"):
        return tree

    # We have not reached a block yet, so go up
    return find_enclosing_fun(tree.parent)