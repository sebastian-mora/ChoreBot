import threading
import schedule
import datetime
from Texter import Texter
from Roommate import Roommate
from flask import Flask, request
import random
import time

roommates = [Roommate("Seb", "+***REMOVED***", [2, 3],[]),
             Roommate("Ed", "+***REMOVED***", [3, 0],[]),
             Roommate("Jake", "+***REMOVED***", [3, 4],[]),
             Roommate("Chase","+***REMOVED***",[0,4] , [])]

weeklyChores = ["Sweep/Mop Common Room",
                "Wipe down kitchen counter and Stove", "Wipe Down Toilet",
                "Remove old Food from fridge",
                "You got lucky no main chore!", "You got lucky no main chore!"]

recurringChores = ["Take out Trash", "Organize the Common Room", "Wash all dishes",
                   "Put away clean dishes"]

doneChores = ["Sweep/Mop Kitchen"]

verificationlist = []  # list of roommates who have reccived verfication texts

date = datetime.datetime.today().weekday()
app = Flask(__name__)

account_sid = '***REMOVED***'
auth_token = '***REMOVED***'

texter = Texter(account_sid, auth_token, '+***REMOVED***')


# This method finds the roommates who signed up for the current weekday and randomly give them a chore
def assignChore():
    for roommate in roommates:

        for day in roommate.days:

            if (day == date):

                if (roommate.chores):  # if roommate did not complete chore give it back to them and shame them
                    shameMessage(roommate)

                randweekly = random.randint(0, len(weeklyChores) - 1)
                randreurring = random.randint(0, len(recurringChores) - 1)

                print("%s IS getting a chore" % roommate.name)

                roommate.chores.append(weeklyChores[randweekly])
                roommate.chores.append(recurringChores[randreurring])
                del weeklyChores[randweekly]
    notifyRoommatesStatus()
    debug()


def debug():
    print "ROOMMATES \n"
    print "\n".join([str(x) for x in roommates])
    print "TODO CHORES\n"
    print "\n".join([str(x) for x in weeklyChores])
    print "DONE CHORES \n"
    print "\n".join([str(x) for x in doneChores])


# Sends message to all non-working roommates
def notifyRoommatesStatus():
    text = ""
    for roommate in roommates:
        if (roommate.chores):
            text = text + "\n" + roommate.name + ": " + str(roommate.chores) + " " + unicode("\u274C ", 'unicode-escape')  # Red Check
        else:
            text = text + "\n" + roommate.name + ": " + unicode("\u2705 ", 'unicode-escape')  # Green Check

    for roommate in roommates:
        texter.sendMessage(roommate.number, text)


def shameMessage(violator):
    for roommate in roommates:
        message = "Your fellow roommate %s failed to complete his chore yesterday!" % violator.name
        texter.sendMessage(roommate.number, message)


def sendVerification(verifier, roommate):
    verificationlist.append(verifier)

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
    if (message_body.lower() == "done" and any(
            roommate.number == sender.number for roommate in roommates)
            and any(
                roommate.chores == sender.chores for roommate in
                roommates)):  # if the sender is a roommate and has chore

        print(" %s Completed his chore requesting verification" % sender)

        for roommate in roommates:
            if (roommate.number is not sender.number):
                print("verification sent to %s", roommate.name)
                sendVerification(roommate, sender)
                if (roommate.number not in verificationlist):  # to prevent dups
                    verificationlist.append(roommate.number)
        texter.sendMessage(sender.number, "Your request is being processed by your roommates")

    elif ("yes" in message_body.lower() and sender.number in verificationlist):
        try:
            name = message_body.split()
            name = name[1]
            if (not any(roommate.name.lower() == name.lower() for roommate in roommates)):  # if the name found is
                # not a person doing chores

                raise Exception

        except:
            texter.sendMessage(sender.number, "Invalid input please use the format (DONE NAME)")

        for roommate in roommates:
            if (name.lower() == roommate.name.lower() and roommate.chores is not None):
                print("Confirmation for %s by %s" % (roommate.name, sender))
                roommate.chores = []
                notifyRoommatesStatus()
                verificationlist.remove(sender)


def resetWeeklyChores():
    weeklyChores.extend(doneChores)
    del doneChores[:]
    print("Reset status: " + str(weeklyChores) + " " + str(roommates))


schedule.every().day.at("9:30").do(assignChore)
schedule.every().monday.do(resetWeeklyChores)

if __name__ == "__main__":
    listener_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    listener_thread.setDaemon(True)
    listener_thread.start()
    resetWeeklyChores()
    print("Starting Chron Job")

    while 1:
        date = datetime.datetime.today().weekday()
        schedule.run_pending()
        time.sleep(5)
