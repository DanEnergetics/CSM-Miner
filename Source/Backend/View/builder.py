from pm4py import util as pmutil
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as log_conversion
from pm4py.objects.log.util import xes as xes_util
from pm4py.objects.log.util import general as log_util


import pandas
import os


log_path = os.path.join(".", "running-example.xes")
log = xes_importer.apply(log_path, {"timestamp_sort" : True})

# parameter assignment
parameters = {}
parameters[pmutil.constants.PARAMETER_CONSTANT_ACTIVITY_KEY] = xes_util.DEFAULT_NAME_KEY
parameters[pmutil.constants.PARAMETER_CONSTANT_TIMESTAMP_KEY] = xes_util.DEFAULT_TIMESTAMP_KEY
parameters[pmutil.constants.PARAMETER_CONSTANT_CASEID_KEY] = log_util.CASE_ATTRIBUTE_GLUE


df = log_conversion.apply(log, parameters, log_conversion.TO_DATAFRAME)
