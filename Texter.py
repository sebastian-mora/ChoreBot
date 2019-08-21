
from twilio.rest import Client
class Texter:


    def __init__(self, account_sid, auth_token, number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.number = number
        self.client = Client(account_sid, auth_token)

    def sendMessage(self, receiver, message):

        message = self.client.messages \
            .create(
            body=message,
            from_=self.number,
            to=receiver)

    def send_message_all(self, roommates, message):
        for roommate in roommates:
            self.sendMessage(roommate['number'], message)

    def notifyRoommatesStatus(self, apt_data):
        roommates = apt_data['roommates']
        text = "To complete your chore please type \"done\" to complete all chores "
        for roommate in roommates:
            if roommate['has_chores']:
                text = text + "\n" + roommate['name'] + ": \n"
                i = 1
                for chore in self.get_chores(roommate['number'], apt_data):
                    text = text + str(i) + ": " + str(chore['name']) + " " + "\u274C " + "\n"# Red Check
                    i+=1
            else:
                text = text + "\n" + roommate['name'] + ": " + "\u2705 " + "\n" # Green Check

        for roommate in roommates:
            self.sendMessage(roommate['number'], text)


    def get_chores(self, number, apt_data):
        chores = apt_data['chores']['weekly_chores']
        yeet = []
        for chore in chores:
            if number == chore['assigned']['number']:
                yeet.append(chore)

        return yeet