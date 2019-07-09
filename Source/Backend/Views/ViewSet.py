import json
from itertools import permutations
from collections import defaultdict

from .View import View, initdoubleDict

class ViewSet(dict):

    def __init__(self):
        super() 


    def addView(self, _View, label):
        self.views.append(_View, label)
   

    def rmView(self,_View):
        if _View in self.views:
            for label, view in self.views.iteritems():
                if view == _View:
                    del self.views[label]


    def rmLabel(self, label):
        del self.views[label]


    def getViews(self):
        return self.views
    

    def getView(self, label):
        return self.views[label]


    def checkLabels(self, view, labelMap):
        """ 
        Function that checks validity of
        label assignments and assigns a
        collective label to unassigned states.

        parameters:
        view -- the View object to take the nodes from
        labelMap -- dictionary of labels and their assigned
            original states

        returns:
        valid labelMap
        """

        # transform subnode lists into sets
        tmp = {key : set(subnodes) for key, subnodes in labelMap.items()}

        # check if given nodes are subset of existent nodes
        original_nodes = set(view.getNodes().keys())
        given_nodes = set.union(*tmp.values())
        print(given_nodes)
        if not given_nodes.issubset(original_nodes):
            raise ValueError("""Label assignment incorrect:"""
                """it contains nodes that are not in the original view!""")

        # go through permutations of labels and check if sets of nodes are disjoint 
        for a, b in permutations(labelMap, 2):
            if not tmp[a].isdisjoint(tmp[b]):
                # if non vanishing intersection exist, give warning
                intersection = tmp[a].intersection(tmp[b])
                raise Warning("""Label assignment faulty:"""
                    """node(s) {} are assigned distinct labels {} and {} at once""".format(intersection, a, b))

        # collect unassigned nodes as difference set
        diff = original_nodes.difference(given_nodes)
        if diff:
            labelMap["unassigned"] = list(diff)

        # finally return label map again
        return labelMap

    
    def partition(self, view, labelMap):
        """ 
        Constructor equivalent function that
        partitions a given View into a ViewSet
        object containing the same nodes in total.

        parameter:
        view -- View to be partitioned
        labelMap -- a dictionary containing labels
            as keys and their values are disjoint
            lists of nodes of the View
        """
        # examine labelMap (unnecessary since parseLabelString() ensures correct format)
        # labelMap = self.checkLabels(view, labelMap)

        print("Nodes: ", type(view.getNodes()))

        # initialize resulting dict
        res = dict.fromkeys(labelMap)

        # add original view
        res["original"] = view

        for label, subnodes in labelMap.items():
            # initialize dictionaries
            nodes = dict.fromkeys(subnodes)
            dirSucc = initdoubleDict(subnodes)

            # preserve indirect successors
            indSucc = initdoubleDict(subnodes)

            for source in subnodes:
                # append nodes under the same label
                nodes[source] = view.getNodes()[source]
                # copy all indirect successors fully
                indSucc[source] = view.getIndir()[source].copy()
                # inner loop to copy double dicts
                for target in subnodes:
                    # append direct and indirect successors
                    dirSucc[source][target] = view.getDirect()[source][target]
                    # (leave in indirect successors)
                    # indSucc[source][target] = view.getIndir()[source][target]

            # initialize node with nodes and successors
            res[label] = View(nodes, dirSucc, indSucc)

        print(res)

        # construct self
        self.update(res)


    def toDict(self):
        res = {}
        # populate dictionary
        for key, view in self.items():
            res[key] = view.toDict()
        return res

    
    def toJson(self):
        return json.dump(self.toDict(), indent=4)

    def toJsonFile(self, pathToJson):
        with open(pathToJson, 'w') as out:
            json.dump(self.toDict(), out)



# parsing label JSON helper
def parseLabelString(labelJSONString):
    """ 
    Helper method that brings JSON strings
    containing a label map in the right format.
    The received JSON string will be in the format:
        { node1 : label1,
          node2 : label2,
          ...
        }

    The required format however is:
        { label1 : [nodes belonging to label1],
          label2 : [nodes belonging to label2],
          ...
        }
    This reformatting is part of this function.

    parameters:
    labelJSONString -- string in JSON format

    returns:
    dict -- dictionary as required by checkLabels
    """
    # load JSON as dictionary
    labels = json.loads(labelJSONString)

    # reformat the dictionary
    labelMap = defaultdict(list)
    for node, label in labels.items():
        # mark empty label seperately
        if label == '':
            label = 'unassigned'

        # add node to label map
        labelMap[label] += [node]

    return labelMap

