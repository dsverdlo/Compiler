
class Tac:
    """Class for three-address-code gen"""
    varPrefix = "_t"
    varNumber = 0
    

    def __init__(self):
        pass

    def getVar(self):
        return "{}{}".format(self.varPrefix, self.varNumber)
    
    def getNextVar(self):
        self.varNumber += 1
        return "{}{}".format(self.varPrefix, self.varNumber)

    def genAssignment(self,y,op,z):
        return "{} := {} {} {}".format(self.getNextVar(), y, op, z)

    def genUnaryAssignment(self,op, y):
        return "{} := {} {}".format(self.getNextVar(), op, y)

    def genCopy(self, x, y):
        return "{} := {}".format(x, y)

    def genUncondLoop(self, l):
        return "goto {}".format(l)

    def genCondLoop(self, x, relop, y, l):
        return "if {} {} {} goto {}".format(x, relop, y, l)

    def genProcCallParam(self, x):
        return "param {}".format(x)

    def genProcCall(self, p, n):
        return "call {},{}".format(p,n)

    def genIndexedAssignment(self, x, y,i):
        if(type(i) == int):
            return "{} := {}[{}]".format(x,y,i)
        else:
            return "{}[{}] := {}".format(x,y,i)
