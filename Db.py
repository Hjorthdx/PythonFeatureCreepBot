import asyncio
import asyncpg


async def myfetch(query):
    conn = await asyncpg.connect(user='postgres', password='MD80N2N!fuHz', database='DiscordData', host='127.0.0.1')
    values = await conn.fetch(query)
    await conn.close()
    return values

# Perhabs ? I'm not sure what is best. Both seem, I mean not so safe. Sql injection xd
async def add_opdut(query):
    sql_query = "UPDATE users SET opdutter = opdutter + 1 WHERE id=" + query
    conn = await asyncpg.connect(user='postgres', password='MD80N2N!fuHz', database='DiscordData', host='127.0.0.1')
    res = await conn.fetch(sql_query)
    await conn.close()
    return res







'''
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()


class Test(Base):
    __tablename__ = "users"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    discordID = Column('discordID', Integer)
    opdutter = Column('opdutter', Integer)
    neddutter = Column('neddutter', Integer)
    prefWorkTimer = Column('prefWorkTimer', Integer)
    prefBreakTimer = Column('prefBreakTimer', Integer)


engine = create_engine(os.getenv("DB_CONNECT_STRING"))
Session = sessionmaker(bind=engine)
session = Session()

session.commit()
session.close()

'''

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
