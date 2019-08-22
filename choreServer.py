import datetime
import threading
import pymongo
from flask import Flask, request
from Texter import Texter
from db_interface import db_interface
from random import sample


app = Flask(__name__)
texter = Texter("XXXX", "XXXX", "+XXX")
date = datetime.datetime.today().weekday()
db = db_interface("mongodb://localhost:27017/", "chorebot", "apts")

# Starts flask server. On get it parses then calls sms_reply to handle the logic
@app.route("/sms", methods=['POST'])
def sms_listener():

    message_body = request.form['Body'].lower()
    sender_number = request.form['From']

    sms_reply(sender_number, message_body)

    return 'OK'

def ticker():
    current_time  = get_time()
    all_apts = db.mycol.find({})

    for apt in all_apts:
        if apt['assign-chore-time'] == current_time:
            assign_chores(apt)



def assign_chores(apt):

    def give_chore(apt_data, roommate):
        chores = apt_data['chores']['weekly_chores']
        for chore in sample(chores, len(chores)):
            if chore['completed'] == False:
                chore['assigned'] = {"name": roommate['name'], "number": roommate['number']}
                roommate['has_chores'] = True
                db.complete_roommate_chores(apt_data, roommate['number'])
                return apt_data

    for roommate in apt['roommates']:
        if date in roommate['days'] and roommate['has_chores'] is False:
            apt = give_chore(apt,roommate)
        texter.notifyRoommatesStatus(apt)


# LOGIC
def sms_reply(sender_number, message_body):

    apartment = db.get_apartment(sender_number)
    sender = db.get_sender(sender_number, apartment)

    # User wants to check off chores
    if 'done' in message_body and db.has_chores(sender_number, apartment):
        texter.send_message_all(apartment['roommates'], "%s would like you to verify that he completed his chores!")

    # User wants to verify chores
    elif 'yes' in message_body:
        try:
            name = message_body.split()[1]

            for roommate in apartment['roommates']:
                if roommate['name'] in name and db.has_chores(roommate, apartment):
                    db.complete_roommate_chores(apartment, roommate)
                    texter.sendMessage(roommate['number'], 'Your chore(s) have been verified!')
                    texter.sendMessage(sender_number, "Thank you! Your request has been processed")

        except:
            texter.sendMessage(sender_number, "Roommate not found")

    else:
        texter.sendMessage(sender, "Command not recognized")


####### DB INTERFACE #################

#TODO THIS SHIT
def sendReminder():
    all_apts = db.mycol.find({})
    current_time = get_time()

    for apt in all_apts:
        pass

def ApartmentReset():
    for apt in db.mycol.find({}):
        db.reset_apt(apt)


def get_time():
    now = datetime.datetime.now()
    return str(datetime.time(now.hour, now.minute))[:5]

if __name__ == "__main__":
    # listener_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    # listener_thread.setDaemon(True)
    # listener_thread.start()
    # assign_chores()
     apt = db.get_apartment("+17072257532")
     db.reset_apt(apt)

