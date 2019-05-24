import json

class View:
    nodes = []
    directSucc = None
    indirectSucc = None

    def __init__(self,_nodes = [],_directSucc= None,_indirectSucc = None):
        self.directSucc = {} if _directSucc == None else _directSucc
        self.nodes = _nodes
        self.indirectSucc = {} if _indirectSucc == None else _indirectSucc
    
    def addNode(self,_Node):
        nodes.append(_Node)

    def addDirectSucc(self,sourceNode, targetNode,frequency):
        if not isinstance(self.directSucc[sourceNode],dict):
            self.directSucc[sourceNode] = {}
        self.directSucc[sourceNode][targetNode] = frequency
    
    def addIndirectSucc(self,sourceNode, targetNode,frequency):
        if not isinstance(self.indirectSucc[sourceNode],dict):
            self.indirectSucc[sourceNode] = {}
        self.indirectSucc[sourceNode][targetNode] = frequency
    

    def getNodes(self):
        return self.nodes
    
    def getIndir(self):
        return self.indirectSucc

    def getDirect(self):
        return self.directSucc

    def toJson(self):
        main = []
        main.append(self.nodes)
        main.append(self.directSucc)
        main.append(self.indirectSucc)
        return json.dumps(main,indent=4)

    def fromJson(jsonString):
        main = json.loads(jsonString)
        try:
            rt = View(main[0],main[1],main[2])
            return rt
        except:    
            return "Error"