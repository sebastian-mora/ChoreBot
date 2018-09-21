'''
1. On start of each day send out chores 
2. send verificaiton
3. listen for verification
4. Remove chores from list
'''

import time
import schedule
import datetime
from twilio.rest import Client
from Roommate import Roommate
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import random

account_sid = '***REMOVED***'
auth_token = '***REMOVED***'

roommates = [Roommate("Ed","+***REMOVED***",[0,3]) , Roommate("Seb", "+***REMOVED***", [1,2])]  
todoChores = ["Sweep Kitchen","Sweep Common Room","Wash All Dishes", "Organize the Common Room", "Wipe down Kitchen counter and Stove", "Put away Washed Dishes","Wipe Down Toilet", "Clean Shower","Sweep Bathroom","Wipe Down Sink and Mirror","Take out Trash","Refill the Water filter"]
doneChores = []
workers = [] #list of roomates with tasks assiged for the day
verificationlist = [] #list of roomates who have reccived verfication texts

date = datetime.datetime.today().weekday()
app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])


#This method finds the roomates who signed up for the current weekday and randonly give them a chore\
def assignChore():
	print("BANG BANG BANG")
	temp = []
	for roommate in roommates:
		for day in roommate.days:
			if(day == date):
				rand = random.randint(0,len(todoChores))
				print("%s IS getting a chore" % roommate.name)
				roommate.chore = todoChores[rand]
				workers.append(roommate)
				roommates.remove(roommate)
				temp.append(todoChores[rand])
				sendChore(roommate,date)
				del todoChores[rand]
	todoChores.extend(temp) #add all the used chores back to the TODO list untill they are verified done




def sendChore(roommate,date):
	client = Client(account_sid, auth_token)
	text = "%s \n Good Morning %s! \n The chore that you have been assigned today is: \n  %s \n please respond DONE when you have completed the chore." %(date,roommate.name,roommate.chore)
	print("%s \n Good Morning %s! \n The chore that you have been assigned today is: \n  %s \n please respond DONE when you have completed the chore." %(date,roommate.name,roommate.chore))
	message = client.messages \
                	.create(
                     	body=text,
                     	from_='+***REMOVED***',
                     	to=roommate.number
                	)
def sendMessage(roommate,message):
	client = Client(account_sid, auth_token)
	message = client.messages \
                	.create(
                     	body=message,
                     	from_='+***REMOVED***',
                     	to=roommate.number
                	)

def sendVerification(verifier,roommate):
	verificationlist.append(verifier)
	client = Client(account_sid, auth_token)
	text = "Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  Please respond (YES %s) if he has completed the chore" % (verifier.name,roommate.name,roommate.chore,roommate.name)
	print("Hello %s! \n Your roommate %s has requested that you verify that he completed %s ! \n  Please respond (YES %s) if he has completed the chore" % (verifier.name,roommate.name,roommate.chore,roommate.name))
	message = client.messages \
                	.create(
                     	body=text,
                     	from_='+***REMOVED***',
                     	to=number
                	)

@app.route('/sms', methods=['POST'])
def sms_reply():
	message_body = request.form['Body']
	number = request.form['From']

	for roommate in roommates:
		if(roommate.number == number):
			sender = roommate

	if(message_body=="DONE"):
		print(" %s Completed his chore requesting verfication" % sender)
		for roommate in roommate:
			if(roommate.chore == None):
				print("verfication sent to %s" , roommate.name)
				sendVerification(roommate,sender)
				verificationlist.append(roommate.number)

	if("YES" in message and number in verificationlist):
		name =  message.split()
		name  =  name[1]

		for worker in workers:
			if(name.lower() == worker.lower()):
				print("Confimation for %s by %s" %(worker.name,name))
				roommate.append(worker)
				workers.remove(worker)
				sendMessage(worker,"Your task has been verified! Thank you!")
				sendMessage(sender, "You have verified %s's task!" % worker.name)
	resp = MessagingResponse()
	resp.message("Ahoy! Thanks so much for your message.")
	return str(resp)







schedule.every().day.at("15:26").do(assignChore)

if __name__ == "__main__":
    assignChore()
    app.run(debug=True)








	

   