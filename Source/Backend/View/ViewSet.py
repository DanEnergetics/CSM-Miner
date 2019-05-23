import json
from View.viewItem import viewItem

class ViewSet:
    head = viewItem()

    def get(self, req, limit = "none"):
        action = req.split('.')
        if limit == "none":
            maxNode = 0
        else :
            maxNode = action.len()-1-limit if action.len()-limit > 0 else 0
        curNode = self.head
        if curNode.getName() != action[0]:
            print("Wrong head selected.")
            return "WHError"
        tempNode = viewItem()
        for i in range(1,action.len() - limit):
            tempNode = curNode.getChild(action[i])
            if curNode.isChild(tempNode):
                print("Going into : " + action[i])
                curNode = tempNode
            else :
                print(action[i] + " is not a child from " + action[i-1] + " complete request was : " + req)
                return "NCError"
        return curNode

    def add(self,_NodeName,_NodeValue,_ParentNode = ""):
        parent = self.get(_ParentNode) if isinstance(_ParentNode,str) else _ParentNode
        n = viewItem(_NodeName,_NodeValue)
        parent.addChild(n)

    def remove(self,req):
        parent = self.get(req,1)
        parent.removeChild(parent.getChild(req.split('.')[req.split('.').len()-1]))
        

    def set(self,name,value):
        node = self.get(name)
        if not isinstance(node,str):
            print("Error while setting, see above")
            return 
        node.setValue(value)


    def clear(self):
        head = viewItem

    def fromJSON(json):
        return ViewSet()

    def toJSON(self):
        return json.dump(self)