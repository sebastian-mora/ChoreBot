import json

class JsonParser:

    def __init__(self,data_file):
        with open(data_file) as f:
            self.data = json.load(f)


    def parseApartments(self):
        i=0
        while(self.data[i] is not None):

           aptname =  self.data[i]["Apt_name"]


