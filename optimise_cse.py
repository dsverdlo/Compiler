#-------------------------------------------------------------------------------
# Name:         optimise_cse.py # UNFINISHED, NOT IN USE
# Purpose:      An expression is a Common Subexpression (CSE) if the expression
#               was previously computed and the values of the operands have not
#               changed since the previous computation
#
# Author:       David Sverdlov
# Course:       Compilers, june 2015
#-------------------------------------------------------------------------------

def optimise_common_subexpression(ast):
    # check if exists
    if not( type(ast) is Node):
        return False

    if ast.data == 'assign': pass

    # walk until assignment is found
    for c in ast.children:
        optimise_common_subexpression(c)
    return False




def check_if_cse_exists(ast, target):
    if not( type(ast) is Node):
        return False

    if ast.data == 'assign':
        if len(ast.children) != len(target.children):
            return check_if_cse_exists(ast.children[0], target) # and other
        for child in ast.children:
            if child != target.children[ast.children.index(child)]:
                return check_if_cse_exists(child)
        return ast

    # walk until assignment is found
    for c in ast.children:
        check_if_cse_exists(c, target)
    return False