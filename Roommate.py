class Roommate:
    days = []
    chore = []

    def __init__(self, name, number, days):
        self.name = name
        self.number = number
        self.days = days

    def getName(self):
        return self.name

    def getNumber(self):
        return self.number



    def __str__(self):
        return str(self.name) + "," + str(self.days) + "," + str(self.chore)
