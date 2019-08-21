
from twilio.rest import Client
import datetime


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
