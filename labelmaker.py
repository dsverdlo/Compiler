class labelmaker(object):
    def __init__(self, fname = ""):
        self.n = 0
        self.fname = fname

    def getLabel(self):
        self.n += 1
        return "L" + str(self.n) + "_" + str(fname)

    def getTempVar(self):
        self.n += 1
        return "_tmp_" + str(self.n)
