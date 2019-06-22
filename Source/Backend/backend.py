import json
import os

from Views import buildViewFromXES
from Views.View import View
from Views.ViewSet import ViewSet, parseLabelString


viewsetJsonPath = "viewset.json"


class BackEnd:


    def call(xes,name):
        print("\033[1;32;40m Back-end call received. \n")
        set_ = buildViewFromXES(xes)
        file_content = set_.toJson()
        _path = str.replace(xes,name,"graph.json")
        FileW = open(_path,"w")
        FileW.write(file_content)
        FileW.close()
        filename = str.replace(xes,name,'') + "index.json"
        old_string = "false"
        new_string = "true"
        with open(filename) as f:
                s = f.read()
        with open(filename, 'w') as f:
                s = s.replace(old_string, new_string)
                f.write(s)


    def partition_call(pathToViewJSON, labelJSONString):
        # read view from file
        # with open(pathToViewJSON, 'r') as input:
        view = View.fromJsonFile(pathToViewJSON)

        indexPath = pathToViewJSON.replace("graph","index")
        old_string = "true"
        new_string = "false"
        with open(indexPath) as f:
                s = f.read()
        with open(indexPath, 'w') as f:
                s = s.replace(old_string, new_string)
                f.write(s)
        # read label map from string and partition the the views
        labelMap = parseLabelString(labelJSONString)
        viewset = ViewSet()
        viewset.partition(view, labelMap)
        # write viewset to JSON file (overwrites view json)
        viewset.toJsonFile(pathToViewJSON) 
        with open(indexPath) as f:
                s = f.read()
        with open(indexPath, 'w') as f:
                s = s.replace(new_string, old_string)
                f.write(s)


# unit tests
if __name__ == "__main__":

    labelString = '["\"register request\": \"a\"","\"examine thoroughly\": \"a\"","\"check ticket\": \"a\"","\"decide\": \"b\"","\"reject request\": \"b\"","\"examine casually\": \"b\"","\"pay compensation\": \"\"","\"reinitiate request\": \"\""]'

    labelString = labelString.replace('\\', '').replace('""', '"').replace('[', '{').replace(']', '}')

    xes = "./Views/running-example.xes"
    name = "running-example.xes"

    BackEnd.call(xes, name)

    viewJSON = "./Views/graph.json" 

    BackEnd.partition_call(viewJSON, labelString)



