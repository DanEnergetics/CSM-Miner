import json
import ViewClass
from ViewClass import View

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
    
    def createViewsForLabelsWithLabels(_View = View(),_Map = None):
        if _Map == None :
           Map = {}
        else :
            Map = _Map
        labels = []
        _ViewSet = ViewSet()
        for a,b in Map:
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
