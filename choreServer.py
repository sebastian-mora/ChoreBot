import threading
import schedule
import datetime
from Texter import Texter
from Roommate import Roommate
from flask import Flask, request
import random
import time

roommates = [Roommate("Seb", "+***REMOVED***", [2, 3]), Roommate("Ed", "+***REMOVED***", [0, 2]),
             Roommate("Jake", "+***REMOVED***", [1, 3]),Roommate("Chase","+***REMOVED***",[1,6]),]




weeklyChores = ["Sweep/Mop Kitchen", "Sweep/Mop Common Room",
                "Wipe down kitchen counter and Stove", "Wipe Down Toilet", "Clean Shower",
                "Remove old Food from fridge",
                "You got lucky no main chore!", "You got lucky no main chore!"]

recurringChores = ["Take out Trash", "Organize the Common Room", "Wash all dishes",
                   "Put away clean dishes"]

doneChores = []

workers = []  # list of roommates with tasks assiged for the day
verificationlist = []  # list of roommates who have reccived verfication texts

date = datetime.datetime.today().weekday()
app = Flask(__name__)

account_sid = '***REMOVED***'
auth_token = '***REMOVED***'

texter = Texter(account_sid,auth_token,'+***REMOVED***')


# This method finds the roommates who signed up for the current weekday and randomly give them a chore
def assignChore():
    temp = []
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
                workers.append(roommate)
                temp.append(weeklyChores[randweekly])
                texter.sendChore(roommate)

                del weeklyChores[randweekly]
    notifyRoommates()

    weeklyChores.extend(temp)  # add all the used chores back to the TODO list until they are verified done
    debug()


def debug():
    print "ROOMMATES \n"
    print "\n".join([str(x) for x in roommates])
    print "WORKERS \n"
    print "\n".join([str(x) for x in workers])
    print "TODO CHORES\n"
    print "\n".join([str(x) for x in weeklyChores])
    print "DONE CHORES \n"
    print "\n".join([str(x) for x in doneChores])



#Sends message to all non-working roommates
def notifyRoommates():
    message = "The roommate(s) who have chores today are: \n"

    for worker in workers:
        message = message + str(worker.name) + ": " + str(worker.chore) + "\n"

    print("Notify Method: %s" % message)

    for roommate in roommates:
        if (roommate not in workers):
            texter.sendMessage(roommate.number, message)


def shameMesage(violator):
    for roommate in roommates:
        if (roommate not in workers):
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
            worker.number == sender.number for worker in workers)):  # Not clear who the sender is
        print(" %s Completed his chore requesting verification" % sender)
        for roommate in roommates:
            if (roommate.number is not sender.number):
                print("verfication sent to %s", roommate.name)
                sendVerification(roommate, sender)
                if (roommate.number not in verificationlist):  # to prevent dups
                    verificationlist.append(roommate.number)
                texter.sendMessage(sender.number, "Your request is being processed by your roommates")

    elif ("YES" in message_body and sender.number in verificationlist):

        try:
            name = message_body.split()
            name = name[1]
            if (not any(worker.name == name for worker in workers)):  # if the name found is not a person doing chores
                raise Exception

        except:
            texter.sendMessage(sender.number, "Invaild input please use the format (DONE NAME)")

        for worker in workers:
            if (name.lower() == worker.name.lower() and worker.chore is not None):
                print("Confirmation for %s by %s" % (worker.name, sender))
                worker.chore = []
                roommates.append(worker)
                workers.remove(worker)
                texter.sendMessage(worker.number, "Your task has been verified! Thank you!")
                texter.sendMessage(sender.number, "You have verified %s's task!" % worker.name)




def resetWeeklyChores():
    weeklyChores.extend(doneChores)
    roommates.extend(workers)
    del doneChores[:]
    del workers[:]
    print("Reset status: " + str(weeklyChores) + " " + str(roommates))


schedule.every().day.at("9:30").do(assignChore)
schedule.every().monday.do(resetWeeklyChores)

if __name__ == "__main__":
    listener_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    listener_thread.setDaemon(True)
    listener_thread.start()
    resetWeeklyChores()
    print("Starting Chron Job")
    assignChore()

    while 1:
        date = datetime.datetime.today().weekday()
        schedule.run_pending()
        time.sleep(5)
