import datetime
import json
import threading
import time

import schedule
from flask import Flask, request

from ChoreManager import ChoreManager
from Roommate import Roommate
from Texter import Texter

with open("config.json") as data_file:
    data = json.load(data_file)

roommates = [Roommate("Seb", "+***REMOVED***", [2, 3], []),
             Roommate("Ed", "+***REMOVED***", [3, 0], []),
             Roommate("Jake", "+***REMOVED***", [3, 4], []),
             Roommate("Chase", "+***REMOVED***", [0, 4], [])]

choremanager = ChoreManager(data["weeklyChores"], data["recurringChores"])

app = Flask(__name__)
texter = Texter(data["account_sid"], data["auth_token"], data["twillo-number"])
date = datetime.datetime.today().weekday()


# This method finds the roommates who signed up for the current weekday and randomly give them a chore
def assignChore():
    for roommate in roommates:
        if (roommate.chores):  # if roommate did not complete chore give it back to them and shame
            shameMessage(roommate)
            roommate.chores.append(choremanager.giveRecurringChore())

        for workday in roommate.days:
            if (workday == date):
                print("%s IS getting a chore" % roommate.name)
                roommate.chores.append(choremanager.giveWeeklyChore())
                roommate.chores.append(choremanager.giveRecurringChore())
    notifyRoommatesStatus()


# Sends message to all non-working roommates
def notifyRoommatesStatus():
    text = ""
    for roommate in roommates:
        if (roommate.chores):
            text = text + "\n" + roommate.name + ": " + str(roommate.chores) + " " + unicode("\u274C ",
                                                                                             'unicode-escape')  # Red Check
        else:
            text = text + "\n" + roommate.name + ": " + unicode("\u2705 ", 'unicode-escape')  # Green Check

    for roommate in roommates:
        texter.sendMessage(roommate.number, text)


def shameMessage(violator):
    for roommate in roommates:
        message = "Your fellow roommate %s failed to complete his chore yesterday! He's be " \
                  "penalized with extra Chores!" % violator.name
        texter.sendMessage(roommate.number, message)


def sendVerification(verifier, roommate):
    message = "Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  Please respond (" \
              "YES %s) if he has completed their daily chores" % (
                  verifier.name, roommate.name, roommate.chores, roommate.name)
    print(
            "Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  Please "
            "respond (YES %s) if he has completed their daily chores" % (
                verifier.name, roommate.name, roommate.chores, roommate.name))

    texter.sendMessage(verifier.number, message)


# Starts flask server. On get it parses then calles sms_reply to handle the logic
@app.route("/sms", methods=['GET', 'POST'])
def sms_listener():

    message_body = request.form['Body']
    number = request.form['From']

    for roommate in roommates:
        if (roommate.number == number):
            sender = roommate

    sms_reply(sender, message_body)
    return str("OK")


def sms_reply(sender, message_body):

    if (message_body.lower() == "done" and sender.chores): #if sender completeing chores

        sender.completionPending = True;
        print(" %s Completed his chore requesting verification" % sender.name)
        for roommate in roommates:
            if (roommate.number is not sender.number):
                print("verification sent to %s", roommate.name)
                sendVerification(roommate, sender)
            else:
                texter.sendMessage(sender.number, "Invalid Input :(")

        texter.sendMessage(sender.number, "Your request is being processed by your roommates")

    elif ("yes" in message_body.lower()):
        try:
            name = message_body.split()
            name = name[1]
            if (not any(roommate.name.lower() == name.lower() for roommate in roommates)):  # if the name found is
                # not a person doing chores
                raise Exception

        except:
            texter.sendMessage(sender.number, "Invalid input please use the format (DONE NAME)")

        for roommate in roommates:
            if (name.lower() == roommate.name.lower() and roommate.completionPending and roommate is not sender):
                # find roomate, check if they are waiting for veifi, make sure its not self veri
                print("Confirmation for %s by %s" % (roommate.name, sender))
                roommate.chores = []
                roommate.completionPending = False;
                notifyRoommatesStatus()
    else:
        texter.sendMessage(sender.number, "Invalid input! Accepted input ""done"" or ""yes (roommate name)"" ")


def sendReminder():
    for roommate in roommates:
        if (roommate.chores):
            texter.sendMessage(roommate.number, "ChoreBot has noticed you haven't done your chores! And "
                                                "so have your roommates!")


schedule.every().day.at(data["assign-chore-time"]).do(assignChore)
schedule.every().day.at(data["chore-reminder-time"]).do(sendReminder)
schedule.every().monday.do(choremanager.resetWeeklyChores)

if __name__ == "__main__":
    listener_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    listener_thread.setDaemon(True)
    listener_thread.start()
    print("Starting Chron Job")
    assignChore()

    while 1:
        date = datetime.datetime.today().weekday()
        schedule.run_pending()
        time.sleep(5)
