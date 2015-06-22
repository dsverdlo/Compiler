
# We have to type check the following nodes:
#
# Assignment, Binary operations, Func calls, returns
def type_check(node):

    def find_type_of_var(tree, varname):

        if(tree.data == "block"):
            print "Block";
