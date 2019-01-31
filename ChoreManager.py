import random

class ChoreManager:

    def __init__(self, weeklyChores, recurringChores):
        self.weeklyChores = weeklyChores
        self.recurringChores = recurringChores;
        self.doneChores = []


    def giveWeeklyChore(self):
        if(self.weeklyChores):
            rand = random.randint(0, len(self.weeklyChores) - 1)
            chore = self.weeklyChores[rand]
            del self.weeklyChores[rand]
            return chore

    def giveRecurringChore(self):
        if(self.recurringChores):
            rand = random.randint(0, len(self.recurringChores) - 1)
            chore = self.recurringChores[rand]
            return chore

    def completeChores(self, chores):

        for chore in chores:
            if chore in self.weeklyChores:
                self.doneChores.append(chore)
                del self.weeklyChores[self.weeklyChores.index(chore)]

    def resetWeeklyChores(self):
        self.weeklyChores.extend(self.doneChores)
        del self.doneChores[:]