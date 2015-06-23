from node import *

# We have to type check the following nodes:
#
# Assignment, Binary operations, Func calls, returns
def type_check(node):
    #print "Type checking ", node
    def find_type_of_var(tree, varname):
        # If not node then false
        if not(type(tree) is Node):
            return type_check(tree)

        # if we reached a block, then check the variables
        if(tree.data == "block"):
            for variable in tree.children[0].children:
                if variable.children[1] == varname:
                    return variable.children[0]
            # if not found, try higher

        # We have not reached a block yet, so go up
        return find_type_of_var(tree.parent, varname)


    def find_type_of_fun(tree):
        # If not node then false
        if not(type(tree) is Node):
            return False

        # if we reached the func declaration, return the type
        if(tree.data == "FUNCTION"):
            return tree.children[0]

        # We have not reached a block yet, so go up
        return find_type_of_fun(tree.parent)

    def find_fun_decl(tree, funname):
        if not(type(tree) is Node):
            return False
        if tree.data == 'program':
            for child in tree.children:
                if child.data == 'FUNCTION' and child.children[1] == funname:
                    return child
        return find_fun_decl(tree.parent, funname)

    def find_type_of_exp(tree):
        print "DEBUG",tree
        if not type(tree) is Node:
            return type_check(tree)

        if tree.data in ['+', '-', '*', '/', 'length']:
            return 'int'

        if tree.data is 'fCall':
            return find_type_of_fun(tree.data, tree.children[0])

        if tree.data in ['or', 'and', 'not', '>', '>=', '<', '<=', '==', '!=']:
            return 'bool'


    if not(type(node) is Node):
        if type(node) is int:
            return 'int'
        elif type(node) is str:
            return 'char'
        elif type(node) is bool:
            return 'bool'
        else:
            return 'unknown'


    if node.data == 'return':
        returnType = find_type_of_var(node.children[0], node.children[0])
        functionType = find_type_of_fun(node)
        if not returnType:
            print "Type check failed, no type found for variable: " + str(node.children[0])
            return False

        if functionType == False:
            print "Type check failed, no type found for function"
            return False

        if returnType == functionType:
            print "OK" + returnType + " " + functionType
            return True

        print "Type check failed, returning [" + returnType +"] when function should return [" + functionType + "]"
        return False


    elif node.data == 'assignment':
        lexpType = find_type_of_var(node, node.children[0])
        if type(node.children[1]) is Node:
            rexpType = find_type_of_exp(node.children[1])
        elif node.children[1] is int:
            print "todo remove"
            rexpType = 'int'
        elif node.children[1] is str:
            print "todo remove"
            rexpType = 'char'

        if lexpType == rexpType:
            return True

        print "Type check failed, you tried assigning a [" + rexpType + "] to variable " + str(node.children[0]) + " which has type [" + lexpType + "]"
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
            if argType != fparamType:
                print "Type check failed, function '" + node.children[0] + "' expected a [" + fparamType + "] as argNo " + str(i+1) + ", but a [" + argType + "] was given"

        return True

    else:
        for c in node.children:
            type_check(c)
