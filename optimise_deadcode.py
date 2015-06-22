from node import *

VERBOSE = True
def printt(*args):
    if VERBOSE:
        for a in args:
            print " - " + a
        
# right now only detects code after a return statement
def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def optimise_dead_code(ast):
    dead_code = []
    if (type(ast) in [str, int]) or ast.is_empty():
        #printt("Dropping ", ast)
        return dead_code
    else:
        return_found = False
        for child in ast.children:
            if (type(child) is Node) and (child.data == 'return') and not(return_found):
                return_found = True
            else:
                if return_found: # return already appeared son
                    dead_code.append(child)
                    printt("Deleting dead code: " + child.toString())
                    ast.children.remove(child)
                
            opt_child = optimise_dead_code(child)
            if(opt_child != []):
                dead_code.append(opt_child)
            
                
    return flatten(dead_code)

