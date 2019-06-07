import json
from Views.View import View

class ViewSet_:
    def __init__(self):
        self.views = {}
    
    def addView(self, _View, label):
        self.views.append(_View, label)
    
    def rmView(self,_View):
        if _View in self.views:
            for label, view in self.views.iteritems():
                if view = _View:
                    del self.views[label]

    def rmLabel(self, label):
        del self.views[label]

    def getViews(self):
        return self.views
    
    def getView(self,Pos):
        if len(self.views) > Pos:
            return self.views[Pos]
    
    def createViewsForLabelsWithLabels(_View = None,_Map = None):
        if _View == None:
            __View = View()
        else:
            __View = _View
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
            _ViewSet.addView(__View)
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
