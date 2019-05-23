class viewItem:
    Name = ""
    Value = ""
    children = []

    def __init__(self,_Name = "null",_Value = "null"):
        self.Name = _Name
        self.Value = _Value

    def getValue(self):
        return self.Value
    
    def getName(self):
        return self.Name

    def setValue(self,_Value):
        self.Value = _Value
    
    def setName(self,_Name):
        self.Name = _Name

    def getChild(self,_StrName):
        returnChild = viewItem()
        for child in children:
            if child.getName() == _StrName:
                returnChild = child
        return returnChild

    def getChildren(self):
        return self.children

    def isChild(self,Node):
        return Node in self.children

    def addChild(self,Node):
        self.children.append(Node)
    
