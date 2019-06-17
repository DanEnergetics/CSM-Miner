import json
from collections import defaultdict

class View:
    nodes = {}
    directSucc = None
    indirectSucc = None

    def __init__(self, nodes = {},_directSucc= None,_indirectSucc = None):
        # initiate nodes
        self.nodes = nodes

        # initiate direct and indirect successors as double dictionaries 
        self.directSucc = initdoubleDict(self.nodes) if _directSucc == None else _directSucc
        self.indirectSucc = initdoubleDict(self.nodes) if _indirectSucc == None else _indirectSucc

    
    def addNode(self,node, params):
        self.nodes[node] = params

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

    def toDict(self):
        res = {}
        res["nodes"] = self.nodes
        res["directSuccessors"] = self.directSucc
        res["indirectSuccessors"] = self.indirectSucc
        return res

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
    


def initdoubleDict(keys):
    """ Helper function to initialize double dict. """
    # initialize first layer
    res = dict.fromkeys(keys)
    for key in res:
        res[key] = defaultdict(int)

    return res
