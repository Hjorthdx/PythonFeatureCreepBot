import Db

class User:

    def __init__(self, name, intUserID, strUserID):
        self.name = name
        self.intUserID = intUserID
        self.strUserID = strUserID

    def AddOpdut(self):
        print("Add opdut")
        #Db.mycol.update_one(
        #    { "Name": self.name },
        #    { "$inc": {"Opdutter": 1}}
        #)

    def removeOpdut(self):
        print("Remove opdut")
        #Db.mycol.update_one(
        #    { "Name": self.name },
        #    { "$inc": {"Opdutter": -1}}
        #)

    def AddNeddut(self):
        print("Add neddut")
        #Db.mycol.update_one(
        #    { "Name": self.name },
        #    { "$inc": {"Neddutter": 1}}
        #)

    def removeNeddut(self):
        print("Remove neddut")
        #Db.mycol.update_one(
        #    { "Name": self.name },
        #    { "$inc": {"Neddutter": -1}}
        #)