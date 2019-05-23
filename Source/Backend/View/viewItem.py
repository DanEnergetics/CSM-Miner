class viewItem:
    Name = ""
    Value = ""
    children = []

    def __init__(self,_Name = "null",_Value = "null"):
        self.Name = _Name
        self.Value = _Value
        self.children = []

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
        for child in self.children:
            if child.getName() == _StrName:
                returnChild = child
        return returnChild

    def getChildren(self):
        return self.children

    def isChild(self,Node):
        return Node in self.children

    def addChild(self,Node = "null",Value = "null"):
        if isinstance(Node,str):
            self.children.append(viewItem(Node,Value))
        else :
            self.children.append(Node)
    
    def removeChild(self,Node):
        self.children.remove(Node)

    def isValueStorage(self):
        return len(self.children) == 0
    
    def toString(self,indent = 0):
        if self.isValueStorage():
            tmp = ""
            for i in range(indent):
                tmp += "\t"
            tmp += "\"" + self.Name + "\"" + " : " + "\"" + self.Value + "\"" 
            return tmp
        else:
            tmp = ""
            for i in range(indent):
                tmp += "\t"
            tmp += "\"" + self.Name + "\"" + " : {\n"
            for m in range(len(self.children)):
                for i in range(indent):
                    tmp += "\t"
                child = self.children[m]
                tmp += child.toString(indent+1)
                print(str(m) + ":" + str(len(self.children)-1))
                if (m+1) in range(len(self.children)):
                    tmp += ","
                tmp += "\n"
            for i in range(indent):
                tmp += "\t"
            tmp += "}"
            return tmp