from twilio.rest import Client
import datetime


class Texter:

    account_sid = None
    auth_token = None
    number = None
    client = None

    def __init__(self, account_sid, auth_token, number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.number = number
        self.client = Client(account_sid, auth_token)

    def sendMessage(self, receiver, message, image):

        if(image is None):

            message = self.client.messages \
                .create(
                body=message,
                from_=self.number,
                to=receiver)
        else:
            message = self.client.messages \
                .create(
                body=message,
                media_url= image,
                from_=self.number,
                to=receiver)


    def sendMessageAll(self, roommates, message, image):

        for roommate in roommates:

            message = self.client.messages \
                .create(
                body=message,
                media_url= image,
                from_=self.number,
                to=roommate.number)


    def sendChore(self, roommate):
        date = datetime.datetime.today().weekday()

        text = "%s \n Good Morning %s! \n \n The chore that you have been assigned today is: \n %s \n\n please respond DONE " \
               "when you have completed the chore." % (date, roommate.name, roommate.chore)
        print(
                "%s \n Good Morning %s! \n The chore that you have been assigned today is: \n %s \n please respond "
                "DONE when you have completed the chore." % (date, roommate.name, roommate.chore))

        self.sendMessage(roommate.number,text,None)


    # Sends message to all non-working roommates
    # TODO reduce this mehtod
    def notifyRoommatesStatus(self,roommates):
        text = "To complete your chore please type done! It is preferred that you add a picture to aid in the " \
               "verification process. \n"
        for roommate in roommates:
            if (roommate.chores):
                text = text + "\n" + roommate.name + ": " + str(roommate.chores) + " " + unicode("\u274C ",
                                                                                                 'unicode-escape')  # Red Check
            else:
                text = text + "\n" + roommate.name + ": " + unicode("\u2705 ", 'unicode-escape')  # Green Check

        for roommate in roommates:
            self.sendMessage(roommate.number, text,None)

    def shameMessage(self, apartment, violator):
        for roommate in apartment.roommates:
            message = "Your fellow roommate %s failed to complete his chore yesterday! He's be " \
                      "penalized with extra Chores!" % violator.name
            self.sendMessage(roommate.number, message,None)

    def sendVerification(self, verifier, roommate,image):
        message = "Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  " \
                  "Please respond (" \
                  "YES %s) if he has completed their daily chores" % (
                      verifier.name, roommate.name, roommate.chores, roommate.name)
        print(
                "Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  Please "
                "respond (YES %s) if he has completed their daily chores" % (
                    verifier.name, roommate.name, roommate.chores, roommate.name))

        self.sendMessage(verifier.number, message,image)