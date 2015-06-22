# back end, optimizing and code gen
#
# http://en.wikipedia.org/wiki/Global_value_numbering
#
#
#
#
from node import *
from optimise_constfold import *
from optimise_deadcode import *
from optimise_cse import *
from optimise_var_use import *
from labelmaker import *


VERBOSE = False
def printt(*args):
    if VERBOSE:
        print args

        
def optimise(ast):
    
    print "Optimising: dead code"
    optimise_dead_code(ast)
    
    print "Optimising: constant folding"
    optimise_constant_fold(ast)
    
    print "Optimising: common subexpression elimination"
    optimise_common_subexpression(ast)

    print "Optimising: var use"
    optimise_var_use(ast)
    
    return ast



# Transforms nodes like x = y * 2 + z
# To tmp_1 = y * 2
#    x = tmp_1 + z
def flatten_instructions(tree, lblmkr = None):
    
    def insert_before_statement(tree, node):
        if not(type(tree.parent) is Node): return
        printt("\ins " + tree.toString())
        if(tree.parent.data == 'STATEMENTS'):
            pos = tree.parent.children.index(tree)
            tree.parent.children.insert(pos, node)
            node.parent = tree.parent
            printt("Done: ", tree.parent)
        else:
            insert_before_statement(tree.parent, node)

    def add_to_declarations(tree, node):
        if not(type(tree) is Node): return
        if(tree.data == 'block'):
            tree.children[0].add_child(node)
            printt("BLOCK: ", tree)
        else:
            add_to_declarations(tree.parent, node)

    def do_flattening(node):
        if not(type(tree) is Node): return

        grabparent = node.parent
        printt(" ; Flattening node: " + str(node) + " of: " + str(node.parent))

        tmpvar = lblmkr.getTempVar()

        decl = Node('var')
        decl.add_child('int') # char??
        decl.add_child(tmpvar)
        add_to_declarations(node, decl)
        printt("--", decl.parent)

            
        assign = Node('assign')
        assign.add_child(tmpvar)
        #assign.add_child('placeholder')
        assign.add_child(node)
        
        
        insert_before_statement(grabparent, assign) # TODO remove one iteration?
        #print "--", assign.parent
                        
        i = grabparent.children.index(node)
        grabparent.children.remove(node) # remove child
        grabparent.children.insert(i, tmpvar) # insert tmp var

        print "Made a temp var [" + str(tmpvar) + "] which substitues: " + node.toString()


        
    def flatten_statement(tree): # tree is a statement at first

        if not(type(tree) is Node): return tree

        if tree.data == 'assign':
            for child in tree.children:
                flatten_statement(child)
            return tree
            
        if tree.data in ['if', 'while']:
            for block in tree.children[1:]: # ignore first child (condition)
                for stmt in block.children[1].children: # [1] is statements
                    printt( "** Found a nested stmt: ", stmt)
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
            
    if lblmkr == None:
	lblmkr = labelmaker()
	
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
    
    



