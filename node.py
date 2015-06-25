#-------------------------------------------------------------------------------
# Name:         node.py
# Purpose:      Abstraction layer for Abstract Syntax Tree Intermediate Repr.
#
# Author:       David Sverdlov
# Course:       Compilers, june 2015
#-------------------------------------------------------------------------------

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



    def is_leaf(self):
        return self.data in ['NUMBER', 'VAR', 'QCHAR', 'BOOL']

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


    def toFileString(self, offset = 0):

        if self.is_empty():
            return ""

        pre = "\n"
        count = offset
        while count > 0:
            pre += "|\t"
            count -= 1

        filestring = pre  +  self.data
        for child in self.children:
            if type(child) is Node:
                filestring += child.toFileString(offset + 1)
            else :
                filestring += pre + "|\t" + str(child)

        return filestring