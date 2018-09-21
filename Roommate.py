from Chore import Chore
class Roommate:
	
	chorecompleted = False
	days = []
	Chore = None


	def __init__(self,name,number,days):
		self.name =name
		self.number = number
		self.days = days


	def getName(self):
		return self.name

	def getNumber(self):
		return self.number

	def setChoreCompleted(self):
		self.chorecompleted = true


