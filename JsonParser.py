import json
from Apartment import Apartment
from Roommate import Roommate

class JsonParser:

    def __init__(self,data_file):
        with open(data_file) as f:
            self.data = json.load(f)


    def parseApartments(self):
        apartments = []
        for i in range(0, int(self.data["len"])): #ghetto way
           apt = "Apt_%d" % i
           aptname =  self.data[apt]["Apt_name"]
           roommates = self.parseRoommates()
           weekleychores = self.data[apt]["chores"][0]["weekly_chores"]
           recchores = self.data[apt]["chores"][0]["recurring_chores"]
           choretime = self.data[apt]["assign-chore-time"]
           remnindertime = self.data[apt]["chore-reminder-time"]


           apartments.append(Apartment(aptname,roommates,weekleychores,recchores,choretime,remnindertime))

        return  apartments


    def parseRoommates(self):
        roommates = []
        for i in range(0, int(self.data["len"])):  # ghetto way
            apt = "Apt_%d" % i
            name  = self.data[apt]["roommates"][0]["name"]
            number = self.data[apt]["roommates"][0]["number"]
            status = self.data[apt]["roommates"][0]["completionPending"]

            days = []
            for day in self.data[apt]["roommates"][0]["days"]:
                days.append(int(day))

            chores = []
            for chore in self.data[apt]["roommates"][0]["chores"]:
                chores.append(chore)

            roommates.append(Roommate(name,number,days,chores))
        return roommates
