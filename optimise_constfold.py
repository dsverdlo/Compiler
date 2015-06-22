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
        print(" - Folding node: " + node.toString() + " by " + str(value))
        i = node.parent.children.index(node)
        node.parent.children.remove(node)
        node.parent.children.insert(i, value)

    def children_ints(node):
        for child in node.children:
            if not(type(child) is int):
                return False
        return True

    def recursive_place(ast, ignore, var, value, stopnode):
        printt("Searching for ["+str(var)+"] to ["+str(value)+"] in tree: " + str(ast))
        if (type(ast) == Node and not(stopnode.data)):
            printt("-- node received: " + str(ast.data))
            if ast.data == var:
                ast.data = value # leaf node
                printt("LEAF NODE SWITCHED")
            else:
                # data is another node
                1+2

            for child in ast.children:
                printt("--- recurception: " + str(child))

                if(ignore in ast.children and
                   (ast.children.index(child) <= ast.children.index(ignore))):
                    printt("--- skipping previous nodes")
                    continue

                if(ast.data == 'assign' and child == var):
                    printt("--- NEW ASSIGNMENT FOUND. STOP REPLACING ["+str(var)+"] by ["+str(value)+"]")
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

    if(type(part) == Node):
        if (part.data == 'assign') and len(part.children) >= 2:
            var = part.children[0]
            if type(part.children[1]) in [int, str]:
                value = part.children[1]
                printt("Got one: " + str(value))
                recursive_place(root, part, var, value, Node(False))
            #elif type(part.children[1]) is Node

            # replace binary instructions
        if part.data == '/' and children_ints(part):
            replace_node(part, part.children[0] / part.children[1])
            optimise_constant_fold(part.parent.parent)
        elif part.data == '*' and children_ints(part):
            replace_node(part, part.children[0] * part.children[1])
            optimise_constant_fold(part.parent.parent)
        elif part.data == '+' and children_ints(part):
            replace_node(part, part.children[0] + part.children[1])
            optimise_constant_fold(part.parent.parent)
        elif part.data == '-' and children_ints(part):
            replace_node(part, part.children[0] - part.children[1])
            optimise_constant_fold(part.parent.parent)

        else:
            for child in part.children:
                optimise_constant_fold(part, child)
    else:
        printt("")
