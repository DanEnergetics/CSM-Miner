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

        # set ready in index.json
        filename = str.replace(xes,name,'') + "index.json"
        remFlag(filename)


    def partition_call(pathToViewJSON, labelJSONString):
        print("Partition call with view file {}".format(pathToViewJSON))
        # read view from file
        view = View.fromJsonFile(pathToViewJSON)

        indexPath = pathToViewJSON.replace("graph","index")
        setFlag(indexPath)

        # read label map from string and partition the the views
        labelMap = parseLabelString(labelJSONString)
        viewset = ViewSet()
        viewset.partition(view, labelMap)

        # rename the view file to original
        newPathToViewJSON = pathToViewJSON.replace("graph", "original")
        os.rename(pathToViewJSON, newPathToViewJSON)

        # write viewset to JSON file (overwrites view json)
        pathToViewSetJSON = pathToViewJSON.replace("original", "graph")
        print(pathToViewSetJSON)
        viewset.toJsonFile(pathToViewSetJSON) 

        # unset flag
        print("Remove flag (set it to true)!")
        remFlag(indexPath)



def setFlag(indexPath):
    """ Mark the request as being processed. """
    old_string = "true"
    new_string = "false"
    with open(indexPath) as f:
            s = f.read()
    with open(indexPath, 'w') as f:
            s = s.replace(old_string, new_string)
            f.write(s)


def remFlag(indexPath):
    """ Mark the request as being processed. """
    old_string = "true"
    new_string = "false"
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



