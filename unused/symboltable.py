# Symbol table

class SymbolTable(object):
    
    def __init__(self, parent = None):
        self.parent = parent
        self.symbols = dict()

    # Adds a symbol in the table
    def addSymbol(self, typ, nam, val = None):
        if self.hasSymbol(nam):
            return False
        self.symbols[nam] = [typ, val]
        return True

    # Check whether the symbol already exists
    def hasSymbol(self, name):
        return name in self.symbols

    # Set / update the value of a symbol
    def setSymbol(self, nam, val):
        if self.hasSymbol(nam):
            return False
        elif type(val) is self.symbols[nam][0]:
            self.symbols[nam][1] = val
            return True

    # Get the value of a symbol
    def getSymbolValue(self, name):
        if self.hasSymbol(name):
            return self.symbols[name][1]
        elif self.parent != None:
            return self.parent.getSymbolValue(name)
        return False

a = SymbolTable()
b = SymbolTable(a)
a.addSymbol(int, 'count', 5)
b.addSymbol(str, 'string', 'HELLO WORLD')

