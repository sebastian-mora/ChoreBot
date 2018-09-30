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
        self.client  = Client(account_sid, auth_token)

    def sendMessage(self, reccivernumber, message):
        message = self.client.messages \
            .create(
            body=message,
            from_=self.number,
            to=reccivernumber)

    def sendChore(self, roommate):
        date = datetime.datetime.today().weekday()

        text = "%s \n Good Morning %s! \n \n The chore that you have been assigned today is: \n %s \n\n please respond DONE " \
               "when you have completed the chore." % (date, roommate.name, roommate.chore)
        print(
                "%s \n Good Morning %s! \n The chore that you have been assigned today is: \n %s \n please respond "
                "DONE when you have completed the chore." % (date, roommate.name, roommate.chore))
        message = self.client.messages \
            .create(
            body=text,
            from_=self.number,
            to=roommate.number
        )

