import random

class ChoreManager:

    def __init__(self,weeklyChores,recurringChores):
        self.weeklyChores = weeklyChores
        self.recurringChores =recurringChores;
        self.doneChores = []


    def giveWeeklyChore(self):
        rand = random.randint(0, len(self.weeklyChores) - 1)
        chore = self.weeklyChores[rand]
        del self.weeklyChores[rand]
        return chore

    def giveRecurringChore(self):
        rand = random.randint(0, len(self.recurringChores) - 1)
        chore = self.weeklyChores[rand]
        return chore

    def completeChore(self, chore):
        self.doneChores.append(chore)

    def resetWeeklyChores(self):
        self.weeklyChores.extend(self.doneChores)
        del self.doneChores[:]