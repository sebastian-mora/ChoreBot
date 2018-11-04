from ChoreManager import ChoreManager


class Apartment:

    def __init__(self, aptname, roommates, weeklychores, recurringchores, choretime, remindertime):

        self.aptname = aptname
        self.choremanager = ChoreManager(weeklychores, recurringchores)
        self.roommates = roommates
        self.choretime = choretime
        self.remindertime = remindertime


    def addRoommate(self,roommate):
        self.roommates.append(roommate)