import json

from Views.ViewFactory import buildViewFromXES
from Views.View import View
from Views.ViewSet import ViewSet




class BackEnd:

    self.viewsetJsonPath = "viewset.json"

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


    def partition_call(pathToViewJSON, pathToPartitionJSON):
        # read view from file
        with open(pathToViewJSON, 'r') as input:
            view = View.fromJSON(input)

        # read state map from file and partition the the views
        with open(pathToPartitionJSON, 'r') as map:
            viewset = ViewSet()
            viewset.partition(view, json.load(map))

        # write viewset to JSON file 
        viewset.toJsonFile(self.viewsetJsonPath) 
