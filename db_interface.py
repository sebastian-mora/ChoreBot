import pymongo

class db_interface:

    def __init__(self, db_url, db_name, db_col):
        self.myclient = pymongo.MongoClient(db_url)
        self.mydb = self.myclient[db_name]
        self.mycol = self.mydb[db_col]

    def get_apartment(self, sender_number):
        apt = self.mycol.find({"roommates": {"$elemMatch": {"number": sender_number}}})
        return apt.next()

    def get_sender(self, sender_number, apt_data):
        for roommate in apt_data['roommates']:
            if roommate['number'] == sender_number:
                return (roommate['name'], sender_number)


    def has_chores(self, number, apt_data):
        chores = apt_data['chores']['weekly_chores']
        for chore in chores:
            if number == chore['assigned']['number'] and chore['completed'] is False:
                return True

    def update_roommate_chores(self, apt_data, roommate):

        changed = False

        for chore in apt_data['chores']['weekly_chores']:
            if roommate['number'] == chore['assigned']['number'] and chore['completed'] is False:
                chore['completed'] = True
                roommate['has_chores'] = False
                changed = True

        if changed:
            self.mycol.update({"_id": apt_data["_id"]}, apt_data)
