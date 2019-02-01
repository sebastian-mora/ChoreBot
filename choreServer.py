import datetime
import threading
import time
import schedule
from flask import Flask, request
from Texter import Texter
from JsonParser import JsonParser

jsonparser = JsonParser("data.json")

apartments = jsonparser.parseApartments()

app = Flask(__name__)
texter = Texter("***REMOVED***", "***REMOVED***", "+***REMOVED***")
date = datetime.datetime.today().weekday()


# This method finds the roommates who signed up for the current weekday and randomly give them a chore
def assignChore():
    for apartment in apartments:
        for roommate in apartment.roommates:
            if (roommate.chores):  # if roommate did not complete chore give it back to them and shame
                texter.shameMessage(apartment, roommate)
                roommate.chores.append(apartment.choremanager.giveWeeklyChore())

            for workday in roommate.days:
                if (workday == date):
                    print("%s IS getting a chore" % roommate.name)
                    roommate.chores.append(apartment.choremanager.giveWeeklyChore())
                    roommate.chores.append(apartment.choremanager.giveRecurringChore())
        texter.notifyRoommatesStatus(apartment.roommates)


# Starts flask server. On get it parses then calles sms_reply to handle the logic
@app.route("/sms", methods=['GET', 'POST'])
def sms_listener():
    message_body = request.form['Body']
    number = request.form['From']

    if(request.form['MediaUrl0'] is not None):
        image_url = request.form['MediaUrl0']
    else:
        image_url = None

    print("Message received (%d,%s,%s)" %(number,message_body,image_url))
    for apartment in apartments:
        for roommate in apartment.roommates:
            if roommate.number == number:
                sender = roommate

    sms_reply(apartment, sender, message_body.lower(), image_url)
    return str("OK")


def sms_reply(apartment, sender, message_body, image_url):
    print "From: %s in apt %s - %s" % (sender.name, apartment.aptname, message_body)

    if message_body.lower() == "done" and sender.chores:  # if sender wants to complete chores

        sender.completionPending = True;
        print(" %s Completed his chore requesting verification" % sender.name)
        for roommate in apartment.roommates:
            if roommate.number is not sender.number:
                print("verification sent to %s", roommate.name)
                texter.sendVerification(roommate, sender, image_url)

        texter.sendMessage(sender.number, "Your request is being processed by your roommates", None)

    elif ("yes" in message_body.lower()):  # if roommate verifies chores or done
        try:
            name = message_body.split()
            name = name[1]
            if (
                    not any(roommate.name.lower() == name.lower() for roommate in
                            apartment.roommates)):  # if the name found is
                # not a person doing chores
                raise Exception

        except:
            texter.sendMessage(sender.number, "Invalid input please use the format (DONE NAME)", None)

        for roommate in apartment.roommates:  # find the person who verified them
            if (name.lower() == roommate.name.lower() and roommate.completionPending and roommate is not sender):
                # find roomate, check if they are waiting for veifi, make sure its not self veri
                print("Confirmation for %s by %s" % (roommate.name, sender))
                texter.notifyRoommatesStatus(apartment.roommates)
                apartment.choremanager.completeChores(roommate.chores)
                roommate.chores = []
                roommate.completionPending = False;

    elif (message_body is None and image_url is not None):  # if picture is sent after initial verification text
        if (sender.completionPending):
            roommates = apartment.roommates
            del roommates[sender]  # remove sender from list
            texter.sendMessageAll(roommates, "", image_url)

    else:
        texter.sendMessage(sender.number, "Invalid input! Accepted input \"done\" or \"yes (roommate name)\" ", None)


def sendReminder():
    for apartment in apartments:
        for roommate in apartment.roommates:
            if (roommate.chores):
                texter.sendMessage(roommate.number, "ChoreBot has noticed you haven't done your chores! And "
                                                    "so have your roommates!", None)


# TODO Make Scheduler pass apartment into needed methods
def scheduler():
    for apartment in apartments:
        schedule.every().day.at(apartment.choretime).do(assignChore)
        schedule.every().days.at(apartment.remindertime).do(sendReminder)
        schedule.every().monday.do(ApartmentReset)


def ApartmentReset():
    for apartment in apartments:
        apartment.choremanager.resetWeeklyChores()


if __name__ == "__main__":
    listener_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    listener_thread.setDaemon(True)
    listener_thread.start()
    print("Starting Chron Job")

    while 1:
        date = datetime.datetime.today().weekday()
        schedule.run_pending()
        time.sleep(5)
