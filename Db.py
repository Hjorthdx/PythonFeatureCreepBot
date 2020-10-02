import psycopg2
import psycopg2.extras

conn = psycopg2.connect(host="localhost", dbname="DiscordData", user="postgres", password="MD80N2N!fuHz")

#with conn:
#    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#        cur.execute("CREATE TABLE user (id SERIAL PRIMARY KEY, name VARCHAR);")
cur = conn.cursor()
#sql = "CREATE TABLE Users (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, discordID integer NOT NULL)"
sql = "INSERT INTO Users(name) VALUES(%s) RETURNING user_id;"
cur.execute(sql, ("Hjorth",))
_id = cur.fetchone()[0]

cur.close()

conn.commit()

conn.close()




'''
import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myClient["mydatabase"]
mycol = mydb["UserKarma"]
pomodoroCol = mydb["Pomodoro"]
wikipediaSpeedrunCol = mydb["WikipediaSpeedrun"]

for document in mycol.find():
    print(document)  

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

'''
