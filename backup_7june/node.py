class Node(object):
    def __init__(self, data = None, parent = None ):
        self.data = data
        self.children = []
        self.parent = parent
        if(parent != None):
            parent.add_child(self)
    
    def is_empty(self):
        self.data == None
        
    def add_child(self, obj):
        self.children.append(obj)
        if(type(obj) is Node):
            obj.parent = self

    def ins_child(self, obj):
        self.children.insert(0, obj)
        if(type(obj) is Node):
            obj.parent = self

##    def __str__(self):
##        children = ""
##        for child in self.children:
##            children += str(self.children.index(child)) + str(child) + ","
##        if(len(children) > 0):
##            children = children.rstrip(",")
##            
##        return "[node(" + self.data + ") children: (" + children + ")]";

        
    def __eq__(self, node):

        # if they are not both nodes -- false
        if(type(node) != type(self)):
            return False

        # if they dont have the same data -- false
        if(node.data != self.data):
            return False

        # if they dont have the same amount of kids -- false
        if(len(self.children) != len(node.children)):
            return False

        # if one of their childs does not match the equivalent -- false
        for child in self.children:
            if(child != node.children[self.children.index(child)]):
                return False

        # otherwise -- true
        return True




                    
    def __str__(self):
        return "<Node: " + self.toString() + ">"
        
    def toString(self):

        if self.is_empty():
            return "(empty)"
        
        sep = ", "
        children = ": "
        for child in self.children:
            try:
                children += child.toString() + sep
            except:
                children += str(child) + sep

        if(len(children) > len(sep)):
            children = children.rstrip(sep)
        else:
            children = children.lstrip(sep)

        if(type(self.data) == type(Node(sep))):
            return "(" + self.data.toString() + children + ")"
        else:
            
            return "(" + str(self.data) + children + ")"
