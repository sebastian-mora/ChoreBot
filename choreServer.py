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

roommates = [Roommate("Ed", "+17072878986", [0, 2]), Roommate("Seb", "+17072257532", [0, 3]), Roommate("Jake","+15593080259",[1,3]), Roommate("Chase","+18053387701",[4,6])]

todoChores = ["Sweep Kitchen", "Sweep Common Room", "Wash All Dishes", "Organize the Common Room",
              "Wipe down Kitchen counter and Stove", "Put away Washed Dishes", "Wipe Down Toilet", "Clean Shower",
              "Sweep Bathroom", "Wipe Down Sink and Mirror", "Take out Trash", "Refill the Water filter"]
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

                if(roommate.chore is not None): #if roommate did not complete chore give it back to them and shame them
                    sendChore(roommate,date)
                    notifyRoommates()

                rand = random.randint(0, len(todoChores))
                print("%s IS getting a chore" % roommate.name)
                roommate.chore = todoChores[rand]
                workers.append(roommate)
                temp.append(todoChores[rand])
                sendChore(roommate, date)
                notifyRoommates()
                del todoChores[rand]

    todoChores.extend(temp)  # add all the used chores back to the TODO list until they are verified done
    debug()

def debug():
    print "ROOMMATES \n"
    print "\n".join([str(x) for x in roommates])
    print "WORKERS \n"
    print  "\n".join([str(x) for x in workers])
    print "TODO CHORES\n"
    print "\n".join([str(x) for x in todoChores])
    print "DONE CHORES \n"
    print "\n".join([str(x) for x in doneChores])

def sendChore(roommate, date):
    client = Client(account_sid, auth_token)
    text = "%s \n Good Morning %s! \n The chore that you have been assigned today is: \n %s \n please respond DONE " \
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


def sendVerification(verifier, roommate):
    verificationlist.append(verifier)
    client = Client(account_sid, auth_token)
    text = "Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  Please respond (" \
           "YES %s) if he has completed the chore" % (
               verifier.name, roommate.name, roommate.chore, roommate.name)
    print(
        "Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  Please "
        "respond (YES %s) if he has completed the chore" % (
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

    if ("YES" in message_body and number in verificationlist):
        name = message_body.split()
        name = name[1]

        for worker in workers:
            if (name.lower() == worker.name.lower() and worker.chore is not None):
                print("Confirmation for %s by %s" % (worker.name, sender))
                worker.chore = None
                roommates.append(worker)
                workers.remove(worker)
                sendMessage(worker, "Your task has been verified! Thank you!")
                sendMessage(sender, "You have verified %s's task!" % worker.name)

    return str("OK")


schedule.every().day.at("9:30").do(assignChore)

if __name__ == "__main__":

    listener_thread = threading.Thread(target=app.run)
    listener_thread.setDaemon(True)
    listener_thread.start()
    print("Starting Chron Job")

    while 1:
        date = datetime.datetime.today().weekday()

        if(date == 0): #on Monday reset all values before starting
            todoChores = todoChores + doneChores
            roommates = roommates + workers
            doneChores = []
            workers = []
            print("Debug status: " + str(todoChores) + " " + str(roommates) )


        schedule.run_pending()
        time.sleep(5)



