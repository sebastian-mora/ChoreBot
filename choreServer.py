'import threading
import schedule
import datetime
from Texter import Texter
from Roommate import Roommate
from flask import Flask, request
import random
import time


roommates = [Roommate("Seb", "+***REMOVED***", [2, 3],[]),
             Roommate("Ed", "+***REMOVED***", [3, 1],[]),
             Roommate("Jake", "+***REMOVED***", [3, 4],[]),
             Roommate("Chase","+***REMOVED***",[1,6] , [])]

weeklyChores = ["Sweep/Mop Kitchen", "Sweep/Mop Common Room",
                "Wipe down kitchen counter and Stove", "Wipe Down Toilet", "Clean Shower",
                "Remove old Food from fridge",
                "You got lucky no main chore!", "You got lucky no main chore!"]

recurringChores = ["Take out Trash", "Organize the Common Room", "Wash all dishes",
                   "Put away clean dishes"]

doneChores = []


verificationlist = []  # list of roommates who have reccived verfication texts

date = datetime.datetime.today().weekday()
app = Flask(__name__)

account_sid = '***REMOVED***'
auth_token = '***REMOVED***'

texter = Texter(account_sid,auth_token,'+***REMOVED***')


# This method finds the roommates who signed up for the current weekday and randomly give them a chore
def assignChore():
    for roommate in roommates:

        for day in roommate.days:

            if (day == date):

                if (roommate.chore):  # if roommate did not complete chore give it back to them and shame them
                    texter.sendChore(roommate)
                    notifyRoommates()

                randweekly = random.randint(0, len(weeklyChores) - 1)
                randreurring = random.randint(0, len(recurringChores) - 1)

                print("%s IS getting a chore" % roommate.name)

                roommate.chore.append(weeklyChores[randweekly])
                roommate.chore.append(recurringChores[randreurring])
                texter.sendChore(roommate)
                del weeklyChores[randweekly]
    notifyRoommates()
    debug()


def debug():
    print "ROOMMATES \n"
    print "\n".join([str(x) for x in roommates])
    print "TODO CHORES\n"
    print "\n".join([str(x) for x in weeklyChores])
    print "DONE CHORES \n"
    print "\n".join([str(x) for x in doneChores])



#Sends message to all non-working roommates
def notifyRoommates():


    message = "The roommate(s) who have chores today are: \n"

    for roommate in roommates:
        if(roommate.chore):
            message = message + str(roommate.name) + ": " + str(roommate.chore) + "\n"

    print("Notify Method: %s" % message)

    for roommate in roommates:
        if (not roommate.chore):
            texter.sendMessage(roommate.number, message)


def shameMesage(violator):
    for roommate in roommates:
        message = "Your fellow roommate %s failed to complete his chore yesterday!" % violator.name
        texter.sendMessage(roommate.number, message)


def sendVerification(verifier, roommate):
    verificationlist.append(verifier)

    message = "Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  Please respond (" \
              "YES %s) if he has completed their daily chores" % (
                  verifier.name, roommate.name, roommate.chore, roommate.name)
    print(
            "Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  Please "
            "respond (YES %s) if he has completed their daily chores" % (
                verifier.name, roommate.name, roommate.chore, roommate.name))

    texter.sendMessage(verifier.number, message)


#Starts flask server. On get it parses then calles sms_reply to handle the logic
@app.route("/sms", methods=['GET', 'POST'])
def sms_listener():
    message_body = request.form['Body']
    number = request.form['From']

    for roommate in roommates:
        if (roommate.number == number):
            sender = roommate

    sms_reply(sender,message_body)
    return str("OK")


def sms_reply(sender,message_body):

    if (message_body.lower() == "done" and any(
            roommate.number == sender.number for roommate in roommates)
            and any(roommate.chore== sender.chore for roommate in roommates)): #if the sender is a roommate and has chore

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
            if (not any(roommate.name.lower() == name.lower() for roommate in roommates)):  # if the name found is not a person doing chores
                raise Exception

        except:
            texter.sendMessage(sender.number, "Invalid input please use the format (DONE NAME)")

        for roommate in roommates:
            if (name.lower() == roommate.name.lower() and roommate.chore is not None):
                print("Confirmation for %s by %s" % (roommate.name, sender))
                roommate.chore = []
                texter.sendMessage(roommate.number, "Your task has been verified! Thank you!")
                texter.sendMessage(sender.number, "You have verified %s's task!" % roommate.name)
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
