from csm.graphs import View, ViewSet
from pm4py import util as pmutil
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as log_conversion
from pm4py.objects.log.util import xes as xes_util
from pm4py.objects.log.util import general as log_util

import json
import urls

import os


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

    # list and dictionaries to represent the view class
    nodes = []
    directSuccessors = {{}}
    indircetSuccessors = {{}}

    # populate list of successors with absolute frequency
    for trace in log:
        for source, target in zip(log, log[1:]):
            # pick only the activity name
            source = source[DEFAULT_NAME_KEY]
            target = target[DEFAULT_NAME_KEY]

            try:
                # increment frequency by 1 if already assigned
                directSuccessors[source][target] += 1
            except KeyError:
                # initialize frequency to 1 if unassigned
                directSuccessors[source][target] = 1


def buildViewSetFromJSON(pathToViewJSON, pathToPartitionJSON):
    # read File
    ViewContent = file_get_contents(pathToViewJSON)
    # to dict
    
    view_list = []
    for view in ViewContent :
        view_list.append(view.fromJson(view)) 
        
    # return view set
    complete = ViewSet()
    for view in view_list:
        complete.addView(complete, view)
    return complete

    
