#-------------------------------------------------------------------------------
# Name:         optimise_constfold.py
# Purpose:      Fold and substitute constant values and constant variables
#
# Author:       David Sverdlov
# Course:       Compilers, june 2015
#-------------------------------------------------------------------------------
from node import *

VERBOSE = False
def printt(*args):
    if VERBOSE:
        for a in args:
            print " - " + a

# Constant folding is the process of recognizing and evaluating
# constant expressions at compile time rather than computing them at runtime.
def optimise_constant_fold(root, part = None):
    printt("Const folding: ", part)
    def replace_node(node, value):
        printt(" - Folding node: {} by {}".format(node,value))
        i = node.parent.children.index(node)
        node.parent.children.remove(node)
        node.parent.children.insert(i, value)
        value.parent = node.parent

    def children_ints(node):
        for child in node.children:
            if child.data != 'NUMBER':
                return False
        return True


    def recursive_place(ast, ignore, var, value, stopnode):
        if (type(ast) == Node and not(stopnode.data)):
            if ast.data == var:
                ast.data = value # leaf node
                printt("LEAF NODE SWITCHED")
            else:
                # data is another node
                1+2

            for child in ast.children:

                if(ignore in ast.children and
                   (ast.children.index(child) <= ast.children.index(ignore))):
                    printt("--- skipping previous nodes")
                    continue

                if(ast.data == 'assign' and child == var):
                    printt("--- NEW ASSIGNMENT FOUND. STOP REPLACING ")
                    stopnode.data = True # stop mechanism
                    return

                # if a child is the var, and we are not in an assign, replace it
                if(child == var):
                    i = ast.children.index(child)
                    ast.children.remove(child)
                    ast.children.insert(i, value)
                    printt("X REPLACED -- new node: " + str(ast))
                else:
                    # else we need to go deeper into nodes
                    if(type(child) == Node):
                        recursive_place(child, ignore, var, value, stopnode)










    if(part is None):
        part = root

    if(type(part) is Node):
        if (part.data == 'assign') and len(part.children) >= 2:

            var = part.children[0]
            if part.children[1].is_leaf() and not(part.children[1].data == 'VAR'):
                value = part.children[1]
                printt("Got one: " + str(value))
                recursive_place(root, part, var, value, Node(False))


            # replace binary instructions
        if part.data == '/' and children_ints(part):
            oldNumber1 = part.children[0].children[0]
            oldNumber2 = part.children[1].children[0]
            newNode = Node('NUMBER')
            newNode.add_child(oldNumber1 / oldNumber2)
            replace_node(part, newNode)
            optimise_constant_fold(part.parent.parent)

        elif part.data == '*' and children_ints(part):
            oldNumber1 = part.children[0].children[0]
            oldNumber2 = part.children[1].children[0]
            newNode = Node('NUMBER')
            newNode.add_child(oldNumber1 * oldNumber2)
            replace_node(part, newNode)
            optimise_constant_fold(part.parent.parent)

        elif part.data == '+' and children_ints(part):
            oldNumber1 = part.children[0].children[0]
            oldNumber2 = part.children[1].children[0]
            newNode = Node('NUMBER')
            newNode.add_child(oldNumber1 + oldNumber2)
            replace_node(part, newNode)
            optimise_constant_fold(part.parent.parent)

        elif part.data == '-' and children_ints(part):
            oldNumber1 = part.children[0].children[0]
            oldNumber2 = part.children[1].children[0]
            newNode = Node('NUMBER')
            newNode.add_child(oldNumber1 - oldNumber2)
            replace_node(part, newNode)
            optimise_constant_fold(part.parent.parent)

        else:
            for child in part.children:
                printt("Optimising child", part, '\n', child)
                optimise_constant_fold(child)
    else:
        printt("else CF")
