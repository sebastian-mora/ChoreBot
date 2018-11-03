from ChoreManager import ChoreManager


class Apartment:

    def __init__(self, roommates, weeklyChores, recurringChores,choretime,remindertime):
        self.choremanager = ChoreManager(weeklyChores, recurringChores)
        self.roommates = roommates
        self.choretime = choretime
        self.remindertime = remindertime


    def addRoommate(self,roommate):
        self.roommates.append(roommate)