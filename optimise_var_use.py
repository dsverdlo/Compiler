#-------------------------------------------------------------------------------
# Name:         optimise_var_use.py
# Purpose:      Remove unused variables
#
# Author:       David Sverdlov
# Course:       Compilers, june 2015
#-------------------------------------------------------------------------------
from node import *

VERBOSE = True
def printt(*arg, **args):
    if VERBOSE:
        for a in arg:
            print " - " + a

def optimise_var_use(ast):

    def check_variable(node, var):
        found = False
        if type(node) is Node:
            children = node.children

            # It does not count if it is the first var in an assignment
            if node.data == 'assign':
                children = node.children[1:]


            for child in children:
                if type(child) is Node:
                    if check_variable(child, var):
                        found = True
                        break
                else:
                    if var == child:
                        found = True
                        break
            return found
        else:
            return var == node

    def delete_assignment(node, var):
        if type(node) is Node:
            if node.data == 'assign':
                if node.children[0] == var:
                    node.parent.children.remove(node)
            else:
                for child in node.children:
                    delete_assignment(child, var)


    if type(ast) is Node:
        if ast.data == 'block':
            children_to_delete = []
            for var in ast.children[0].children:
                varname = var.children[1]
                if not check_variable(ast.children[1], varname):
                    children_to_delete.append(var)

            for var in reversed(children_to_delete):
                varname = var.children[1]
                var.parent.children.remove(var)
                delete_assignment(ast.children[1], varname)
                printt("Removed VARIABLE: " + str(varname) + " since it was not used")
                #print " ******* ", ast

        else:
            for child in ast.children:
                optimise_var_use(child)



