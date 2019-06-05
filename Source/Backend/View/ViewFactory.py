from pm4py import util as pmutil
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as log_conversion
from pm4py.objects.log.util import xes as xes_util
from pm4py.objects.log.util import general as log_util
from ViewClass import View

import os
from itertools import product


def buildViewFromXES(pathToXES):
    """ Populate a new View Object by a given XES.
    All direct and indirect successors are extracted with their respective
    conditional, relative frequency.

    Keyword arguments:
    pathToXES -- the location of the XES file
    """

    # load log file into log object
    log_path = os.path.join(".", "running-example.xes")
    log = xes_importer.apply(log_path, {"timestamp_sort" : True})

    # get occurring activities
    nodes = getNodes(log)

    # get direct successors
    dirSucc = getDirectSuccessors(log, nodes)
    
    # get indirect successors
    indirSucc = getIndirectSuccessors(log, nodes)

    # initialize view object
    return View(nodes, dirSucc, indirSucc)


def getNodes(log):
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

    return set(nodes)


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
    directSuccessors = dict.fromkeys(nodes, dict.fromkeys(nodes, 0))

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
    """
    # normalize frequencies on source state frequency
    for source, target in product(nodes, repeat=2):
        if sourceFreq[source] != 0:
            directSuccessors[source][target] = 39 #directSuccessors[source][target] / sourceFreq[source]
        else:
            directSuccessors[source][target] = 0
    """
    # return normalized frequencies
    return directSuccessors, sourceFreq
               

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
    indirectSuccessors = dict.fromkeys(nodes, dict.fromkeys(nodes, 0))

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
    """
    # normalize frequencies on source state frequency
    for source, target in product(nodes, repeat=2):
        indirectSuccessors[source][target] /= sourceFreq[source]
    """  
    # return normalized frequencies
    return indirectSuccessors
