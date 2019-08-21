import datetime
import threading
import pymongo
from flask import Flask, request
from Texter import Texter
from db_interface import db_interface
from random import shuffle


app = Flask(__name__)
texter = Texter("***REMOVED***", "***REMOVED***", "+***REMOVED***")
date = datetime.datetime.today().weekday()
db = db_interface("localhost:27017", "chorebot", "apt")



# Starts flask server. On get it parses then calls sms_reply to handle the logic
@app.route("/sms", methods=['POST'])
def sms_listener():

    message_body = request.form['Body'].lower()
    sender_number = request.form['From']

    sms_reply(sender_number, message_body)

    return 'OK'

def assign_chores():

    def give_chore(apt_data, roommate):

        for chore in shuffle(apt_data['chores']['weekly_chores']):
            if chore['completed'] == False:
                chore['assigned'] = {"name": roommate['name'], "number": roommate['number']}
                return apt_data



    all_apts = db.mycol.find({})
    current_time = '09:30'

    # TODO Add random selection for more than one chore
    for apt in all_apts:
        if apt['assign-chore-time'] == current_time:
            for roommate in apt['roommates']:
                if date in roommate['days']:
                    apt = give_chore(apt,roommate)





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
                    db.update_roomate_chores(apartment, roommate['number'])
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
    current_time = '09:30'

    # TODO Add random selection for more than one chore
    for apt in all_apts:
        pass

# TODO THIS SHIT
def ApartmentReset():
    pass


if __name__ == "__main__":
    # listener_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    # listener_thread.setDaemon(True)
    # listener_thread.start()
    pass