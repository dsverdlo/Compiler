#-------------------------------------------------------------------------------
# Name:         labelmaker.py
# Purpose:      Create labels and names for temporary variables
#
# Author:       David Sverdlov
# Course:       Compilers, june 2015
#-------------------------------------------------------------------------------
class labelmaker(object):
    def __init__(self, fname = ""):
        self.n = 0
        self.fname = fname

    def getLabel(self):
        self.n += 1
        return "L{}_{}".format(self.n,self.fname)

    def getTempVar(self):
        self.n += 1
        return "_tmp_{}".format(self.n)
