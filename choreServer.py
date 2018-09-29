import threading
import schedule
import datetime
from twilio.rest import Client
from Roommate import Roommate
from flask import Flask, request
import random
import time


account_sid = 'AC6ca4c88efe5765fece8df0c5efb47c37'
auth_token = '090e0eb4c5695b12007c86caaed97f31'

roommates = [Roommate("Seb", "+17072257532", [5, 3]) , Roommate("Jake","+15593080259",[1,3]),
             Roommate("Jake", "+15593080259", [1, 3]),Roommate("Chase","+18053387701",[4,6]),
             Roommate("Ed", "+17072878986", [0, 2])]





weeklyChores = ["Sweep/Mop Kitchen", "Sweep/Mop Common Room",
              "Wipe down kitchen counter and Stove", "Wipe Down Toilet", "Clean Shower", "Remove old Food from fridge",
                "You got lucky no main chore!","You got lucky no main chore!"]

recurringChores = ["Take out Trash","Organize the Common Room","Wash all dishes",
                   "Put away clean dishes"]

doneChores = []

workers = []  # list of roommates with tasks assiged for the day
verificationlist = []  # list of roommates who have reccived verfication texts

date = datetime.datetime.today().weekday()
app = Flask(__name__)


# This method finds the roommates who signed up for the current weekday and randonly give them a chore\
def assignChore():
    temp = []
    for roommate in roommates:

        for day in roommate.days:

            if (day == date):

                if (roommate.chore): #if roommate did not complete chore give it back to them and shame them
                    sendChore(roommate,date)
                    notifyRoommates()

                randweekly = random.randint(0, len(weeklyChores) - 1)
                randreurring = random.randint(0, len(recurringChores) - 1)

                print("%s IS getting a chore" % roommate.name)

                roommate.chore.append(weeklyChores[randweekly])
                roommate.chore.append(recurringChores[randreurring])
                workers.append(roommate)
                temp.append(weeklyChores[randweekly])
                sendChore(roommate, date)

                del weeklyChores[randweekly]
    notifyRoommates()


    weeklyChores.extend(temp)  # add all the used chores back to the TODO list until they are verified done
    debug()

def debug():
    print "ROOMMATES \n"
    print "\n".join([str(x) for x in roommates])
    print "WORKERS \n"
    print  "\n".join([str(x) for x in workers])
    print "TODO CHORES\n"
    print "\n".join([str(x) for x in weeklyChores])
    print "DONE CHORES \n"
    print "\n".join([str(x) for x in doneChores])

def sendChore(roommate, date):
    client = Client(account_sid, auth_token)
    text = "%s \n Good Morning %s! \n \n The chore that you have been assigned today is: \n %s \n\n please respond DONE " \
           "when you have completed the chore." % (date, roommate.name, roommate.chore)
    print(
        "%s \n Good Morning %s! \n The chore that you have been assigned today is: \n %s \n please respond "
        "DONE when you have completed the chore." % (date, roommate.name, roommate.chore))
    message = client.messages \
        .create(
        body=text,
        from_='+16506956346',
        to=roommate.number
)


def sendMessage(roommate, message):
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=message,
        from_='+16506956346',
        to=roommate.number
)

def notifyRoommates():
    client = Client(account_sid, auth_token)

    text = "The roommate(s) who have chores today are: \n"

    for worker in workers:
        text = text + str(worker.name) + ": " + str(worker.chore) + "\n"

    print("Noify Method: %s" % text )

    for roommate in roommates:
        if(roommate not in workers):
            message = client.messages \
                .create(
                body=text,
                from_='+16506956346',
                to=roommate.number
            )

def shameMesage(violater):
    client = Client(account_sid, auth_token)

    for roommate in roommates:
        if(roommate not in workers):
            text = "Your fellow roommate %s failed to complete his chore yesterday!" % violater.name
            message = client.messages \
                .create(
                body=text,
                from_='+16506956346',
                to=roommate.number
        )
#pls git

def sendVerification(verifier, roommate):
    verificationlist.append(verifier)
    client = Client(account_sid, auth_token)
    text = "Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  Please respond (" \
           "YES %s) if he has completed their daily chores" % (
               verifier.name, roommate.name, roommate.chore, roommate.name)
    print(
        "Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  Please "
        "respond (YES %s) if he has completed their daily chores" % (
            verifier.name, roommate.name, roommate.chore, roommate.name))
    message = client.messages \
        .create(
        body=text,
        from_='+16506956346',
        to=verifier.number
        )


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    message_body = request.form['Body']
    number = request.form['From']

    for roommate in roommates:
        if (roommate.number == number):
            sender = roommate

    print(message_body)


    if (message_body.lower() == "done" and any(worker.number == number for worker in workers)): #Not clear who the sender is
        print(" %s Completed his chore requesting verfication" % sender)
        for roommate in roommates:
            if (roommate.number is not sender.number):
                print("verfication sent to %s", roommate.name)
                sendVerification(roommate, sender)
                verificationlist.append(roommate.number)
                sendMessage(sender,"Your request is being processed by your roommates")

    if ("YES" in message_body and number in verificationlist):

        try:
            name = message_body.split()
            name = name[1]
        except:
            sendMessage(sender, "Invaild input please use the format (DONE NAME)")

        for worker in workers:
            if (name.lower() == worker.name.lower() and worker.chore is not None):
                print("Confirmation for %s by %s" % (worker.name, sender))
                worker.chore = []
                roommates.append(worker)
                workers.remove(worker)
                sendMessage(worker, "Your task has been verified! Thank you!")
                sendMessage(sender, "You have verified %s's task!" % worker.name)

    return str("OK")

def resetWeeklyChores():
    weeklyChores.extend(doneChores)
    roommates.extend(workers)
    del doneChores[:]
    del workers[:]
    print("Reset status: " + str(weeklyChores) + " " + str(roommates))

schedule.every().day.at("9:30").do(assignChore)
schedule.every().monday.do(resetWeeklyChores)

if __name__ == "__main__":
    listener_thread = threading.Thread(target=app.run,kwargs={'host':'0.0.0.0'})
    listener_thread.setDaemon(True)
    listener_thread.start()
    #assignChore()
    resetWeeklyChores()
    assignChore()
    print("Starting Chron Job")

    while 1:
        date = datetime.datetime.today().weekday()
        schedule.run_pending()
        time.sleep(5)



