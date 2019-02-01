class Roommate:

    #
    def __init__(self, name, number, days, chores):
        self.name = name
        self.number = number
        self.days = days
        self.chores = chores
        self.completionPending = []


    def getName(self):
        return self.name

    def getNumber(self):
        return self.number

    def __str__(self):
        return str(self.name) + "," + str(self.days) + "," + str(self.chores)
