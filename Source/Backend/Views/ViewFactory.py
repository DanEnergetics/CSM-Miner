from .View import View, initdoubleDict
#from .ViewSet import ViewSet

from pm4py import util as pmutil
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as log_conversion
from pm4py.objects.log.util import xes as xes_util
from pm4py.objects.log.util import general as log_util

import json
from collections import Counter
import os
from itertools import product


def buildViewFromXES(pathToXES, counts=True, costs=True):
    """ Populate a new View Object by a given XES.
    All direct and indirect successors are extracted with their respective
    conditional, relative frequency.

    Keyword arguments:
    pathToXES -- the location of the XES file

    returns:
    View -- an appropriately populated View object
    """

    # load log file into log object
    log_path = pathToXES
    log = xes_importer.apply(log_path, {"timestamp_sort" : True})

    # get occurring activities
    nodes = getNodes(log, counts, costs)

    # get direct successors
    dirSucc = getDirectSuccessors(log, nodes)
    
    # get indirect successors
    indirSucc = getIndirectSuccessors(log, nodes)

    # initialize view object
    return View(nodes, dirSucc, indirSucc)


def loadSampleLog():
    """ Returns a sample log object for debuggin purposes. """
    log_path = os.path.join(".", "running-example.xes")
    return xes_importer.apply(log_path, {"timestamp_sort" : True})


def getNodes(log, counts, costs):
    """ Helper function that extracts all occuring activities from
    passed log file. 
    
    Keyword arguments:
    log -- pm4py log object

    returns:
    set -- set of activities
    dict(dict) -- initialized dict
    """
    # populate nodes inline
    nodes = [event[xes_util.DEFAULT_NAME_KEY] 
                for trace in log
                for event in trace]

    res = {node: {} for node in nodes}
    
    # count occurences of node
    if counts:
        for node in res:
            res[node]["count"] = nodes.count(node)

    # compute average cost of node
    unavail_keyword = "unavailable"
    if costs:
        # calculate cumulated costs
        for trace in log:
            for event in trace:
                # get node identifier
                node = event[xes_util.DEFAULT_NAME_KEY]
                
                # decide wether costs are available and increment value
                if "Costs" in event:
                    if not "costs" in res[node]:
                        res[node]["costs"] = int(event["Costs"])
                    elif res[node]["costs"] != unavail_keyword:
                        res[node]["costs"] += int(event["Costs"])
                else:
                    res[node]["costs"] = unavail_keyword

        # average costs per node if available
        for node in res:
            if res[node]["costs"] != unavail_keyword:
                res[node]["costs"] /= nodes.count(node)


    return res


def getDirectSuccessors(log, nodes):
    """ Helper function that computes the direct successors.

    Keyword arguments:
    log -- pm4py log object to extract information from
    nodes -- the set of nodes

    returns:
    dict -- dictionary where the keys are source states
        and the values are again dictionaries where the
        keys are the directly succeeding target states
        and the values are the relative frequency
    """
    # make initialization from set of nodes
    directSuccessors = initdoubleDict(nodes)

    # absolute source state frequency for later normalization
    sourceFreq = dict.fromkeys(nodes, 0)

    # populate list of successors with absolute frequency
    for trace in log:
        for source, target in zip(trace, trace[1:]):
            # pick only the activity name
            source = source[xes_util.DEFAULT_NAME_KEY]
            target = target[xes_util.DEFAULT_NAME_KEY]

            # increment observation count 
            directSuccessors[source][target] += 1.0

            # increment count of source state
            sourceFreq[source] += 1.0

    # normalize frequencies on source state frequency
    for source, target in product(nodes, repeat=2):
        if sourceFreq[source] != 0:
            directSuccessors[source][target] = round(directSuccessors[source][target] / sourceFreq[source], 2)
        else:
            directSuccessors[source][target] = 0
    # return normalized frequencies 
    return directSuccessors
               

def getIndirectSuccessors(log, nodes):
    """ Helper function that computes the indirect successors.

    Keyword arguments:
    log -- pm4py log object to extract information from
    nodes -- the set of nodes
    returns:
    dict -- dictionary where the keys are source states
        and the values are again dictionaries where the
        keys are the indirectly succeeding target states
        and the values are the relative frequency
    """
    # make initialization from set of nodes
    indirectSuccessors = initdoubleDict(nodes)

    # absolute source state frequency for later normalization
    sourceFreq = dict.fromkeys(nodes, 0)

    # populate list of successors with absolute frequency
    for trace in log:
        for i, j in product(range(len(trace)), repeat=2):
            if i < j-1:
                # pick only the activity name
                source = trace[i][xes_util.DEFAULT_NAME_KEY]
                target = trace[j][xes_util.DEFAULT_NAME_KEY]

                # increment observation count 
                indirectSuccessors[source][target] += 1

                # increment count of source state
                sourceFreq[source] += 1

    # normalize frequencies on source state frequency
    for source, target in product(nodes, repeat=2):
        if sourceFreq[source] != 0:
            indirectSuccessors[source][target] = round(indirectSuccessors[source][target] / sourceFreq[source], 2)
        else:
            indirectSuccessors[source][target] = 0

    # return normalized frequencies
    return indirectSuccessors


def buildViewSetFromJSON(pathToViewJSON, pathToPartitionJSON):
    # read File
    ViewContent = json.loads(file_get_contents(pathToViewJSON))
    

    view_list = []
    for view in ViewContent :
        view_list.append(view.fromJson(view)) 
        
    # return view set
    complete = ViewSet()
    for view in view_list:
        complete.addView(view)
        
    return complete


if __name__ == "__main__":
    # build View
    view = buildViewFromXES("running-example.xes", counts=True)
    print(view.getNodes())
    quit()

    labelMap = {"examine": ["examine thoroughly", "examine casually"]}

    print("Examine casually (node):", view.getIndir()["examine casually"])

    # partition view
    vs = ViewSet()
    vs.partition(view, labelMap)

    print(vs.toDict())
    
