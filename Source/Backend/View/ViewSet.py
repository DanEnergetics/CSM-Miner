import json

class ViewSet:
    views = []
    def __init__(self):
        self.views = []
    
    def addView(self,_View):
        self.views.append(_View)
    
    def rmView(self,_View):
        if _View in self.views:
            self.views.remove(_View)

    def getViews(self):
        return self.views
    
    def getView(self,Pos):
        if len(self.views) > Pos:
            return self.views[Pos]
    
    def createViewsForLabelsWithLabels(_View = View(),_Map = {}):
        labels = []
        _ViewSet = ViewSet()
        for a,b in _Map:
            if not a in labels:
                labels.append(a)
        for i in range(len(labels)):
            _ViewSet.addView(_View)
        return [_ViewSet,labels]


    def partition(_View,_Map):
        main = createViewsForLabelsWithLabels(_View,_Map)
        for i in range(len(main[1])):
            for element in main[0].getView(i):
                for a,b in element.getDirect():
                    if _Map[a] != main[1][i] or _Map[b] != main[1][i] :
                        del element.directSucc[a]
                        if _Map[a] != main[1][i]:
                            element.nodes.remove(a)





class View:
    nodes = []
    directSucc = {{}}
    indirectSucc = {{}}

    def __init__(self,_nodes = [],_directSucc= {{}},_indirectSucc = {{}}):
        self.nodes = _nodes
        self.directSucc = _directSucc
        self.indirectSucc = _indirectSucc
    
    def addNode(self,_Node):
        nodes.append(_Node)

    def addDirectSucc(self,sourceNode, targetNode,frequency):
        self.directSucc[sourceNode][targetNode] = frequency
    
    def addIndirectSucc(self,sourceNode, targetNode,frequency):
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
        return json.dumps(main,indent=4,sort_keys=True)

    def fromJson(jsonString):
        main = json.loads(jsonString)
        try:
            rt = View(main[0],main[1],main[2])
            return rt
        except:    
            return "Error"
