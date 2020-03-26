import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myClient["mydatabase"]
mycol = mydb["UserKarma"]

if not mycol.find():
    karmaList = [
    {"Name": "Adil", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Chrille", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Hjorth", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Martin", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Magnus", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Simon", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Sten", "Opdutter": 0, "Neddutter": 0}
    ]
    x = mycol.insert_many(karmaList)
    print(x.inserted_ids)
