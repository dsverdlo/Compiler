#-------------------------------------------------------------------------------
# Name:         backend.py
# Purpose:      Flatten instructions for IR and provide optimisations
#
# Author:       David Sverdlov
# Course:       Compilers, june 2015
#-------------------------------------------------------------------------------
from node import *
from optimise_constfold import *
from optimise_deadcode import *
from optimise_cse import *
from optimise_var_use import *
from labelmaker import *
import typechecker


VERBOSE = False
def printt(*args):
    if VERBOSE:
        print args


def optimise(ast):

    print "Optimising: dead code"
    optimise_dead_code(ast)

    print "Optimising: constant folding"
    optimise_constant_fold(ast)

    #print "Optimising: common subexpression elimination"
    #optimise_common_subexpression(ast)

    print "Optimising: var use"
    optimise_var_use(ast)

    return ast



# Transforms nodes like x = y * 2 + z
# To tmp_1 = y * 2
#    x = tmp_1 + z
def flatten_instructions(tree, lblmkr, errors):

    def insert_before_statement(tree, node):
        if not(type(tree.parent) is Node) or tree.parent.is_leaf(): return
        printt("\ins {}".format(tree))
        if(tree.parent.data == 'statements'):
            pos = tree.parent.children.index(tree)
            tree.parent.children.insert(pos, node)
            node.parent = tree.parent
            printt("Done: {}".format(tree.parent))
        else:
            insert_before_statement(tree.parent, node)

    def add_to_declarations(tree, node):
        if not(type(tree) is Node) or tree.is_leaf(): return
        if(tree.data == 'block'):
            tree.children[0].add_child(node)
            printt("BLOCK: {}".format(tree))
        else:
            add_to_declarations(tree.parent, node)

    def do_flattening(node):
        if not(type(tree) is Node): return

        grabparent = node.parent

        tmpvarname = lblmkr.getTempVar()
        tmpvarnode = Node('VAR')
        tmpvarnode.add_child(tmpvarname)
        tmpvarnode.parent = grabparent

        decl = Node('varDecl')
        decl.add_child(typechecker.find_type_of_exp(node, errors))
        decl.add_child(tmpvarname)
        add_to_declarations(node, decl)
        printt("--", decl.parent)


        assign = Node('assign')
        assign.add_child(tmpvarnode)
        assign.add_child(node)


        insert_before_statement(grabparent, assign)

        i = grabparent.children.index(node)
        grabparent.children.remove(node) # remove child
        grabparent.children.insert(i, tmpvarnode) # insert tmp node

        return node



    def flatten_statement(tree): # tree is a statement at first

        if not(type(tree) is Node) or tree.is_leaf(): return tree

        if tree.data == 'assign':
            for child in tree.children:
                flatten_statement(child)
            return tree

        if tree.data in ['if', 'while']:
            cond = tree.children[0]
            if(type(cond) is Node) and not(tree.children[0].is_leaf()): pass
                # dont flatten conditions...
                #new = do_flattening(tree.children[0])
                #flatten_statement(new)

            for block in tree.children[1:]: # ignore first child (condition)
                # THEN / ELSE STATEMENTS can be 'exp' or 'block'
                if(block.data != 'block'): continue
                for stmt in block.children[1].children: # [1] is statements
                    printt( "** Found a nested stmt: ", stmt)
                    flatten_statement(stmt)
            return tree

        # Otherwise we can probably substitute some parts
        for child in tree.children:
            if(type(child) is Node) and not(child.is_leaf()): # foreach child that is a node
                # Replace with temp var
                do_flattening(child)
                flatten_statement(child) # iterate to go deeper in stmt
        return tree

    if(type(tree) is Node) and not(tree.is_leaf()):
        if(tree.data == 'statements'):
            for statement in tree.children:
                flatten_statement(statement)

            return tree # done, no more iterating
        else:
            for child in tree.children:
                flatten_instructions(child, lblmkr, errors) # iterate deeper
        return tree
    else:
        return tree# leaf node, do nothing





