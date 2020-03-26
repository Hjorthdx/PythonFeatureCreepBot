import Db

class User:

    def __init__(self, name, intUserID, strUserID):
        self.name = name
        self.intUserID = intUserID
        self.strUserID = strUserID

    def AddOpdut(self):
        Db.mycol.update_one(
            { "Name": self.name },
            { "$inc": {"Opdutter": 1}}
        )

    def removeOpdut(self):
        Db.mycol.update_one(
            { "Name": self.name },
            { "$inc": {"Opdutter": -1}}
        )

    def AddNeddut(self):
        Db.mycol.update_one(
            { "Name": self.name },
            { "$inc": {"Neddutter": 1}}
        )

    def removeNeddut(self):
        Db.mycol.update_one(
            { "Name": self.name },
            { "$inc": {"Neddutter": -1}}
        )