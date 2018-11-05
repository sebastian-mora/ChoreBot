import json
from Apartment import Apartment

class JsonParser:

    def __init__(self,data_file):
        with open(data_file) as f:
            self.data = json.load(f)


    def parseApartments(self):
        apartments = []
        for i in range(0, int(self.data["len"])): #ghetto way
           apt = "Apt_%d" % i
           aptname =  self.data[apt]["Apt_name"]
           roommates = self.data[apt]["roommates"]
           weekleychores = self.data[apt]["chores"][0]
           recchores = self.data[apt]["chores"][1]
           choretime = self.data[apt]["assign-chore-time"]
           remnindertime = self.data[apt]["chore-reminder-time"]


           apartments.append(Apartment(aptname,roommates,weekleychores,recchores,choretime,remnindertime))

        return  apartments


    def test(self):
        return self.data["Apt_0"]["chores"][0]