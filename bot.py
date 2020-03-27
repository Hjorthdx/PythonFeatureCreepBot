import os
import discord
import pymongo
import User
import Db
import threading
import time
from dotenv import load_dotenv

load_dotenv()

# TODO
# Add pomodoro timer
# Add another collection in the database to track how long we are working for, just like lønnes ui in his 

# Emotes
kurtApproved = 619818932475527210
kurtDisapproved = 651028634945060864

#Instantiating all the users
Adil = User.User('Adil', 100552145421467648, '100552145421467648')
Chrille = User.User('Chrille', 279307446009462784, '279307446009462784')
Hjorth = User.User('Hjorth', 140195461519769601, '140195461519769601')
Martin = User.User('Martin', 103033943464353792, '502882469721407509')
Magnus = User.User('Magnus', 272507977984901120, '272507977984901120')
Simon = User.User('Simon', 619105357473775636, '619105357473775636')
Sten = User.User('Sten', 502882469721407509, '502882469721407509')

users = [
    Adil,
    Chrille,
    Hjorth,
    Martin,
    Magnus,
    Simon,
    Sten
]

client = discord.Client()

@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 619105859615719434: 
        if payload.emoji.id == kurtApproved:
            message = await client.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            authorDict = message["author"]
            authorID = authorDict["id"] # String

            for user in users:
                if user.strUserID == authorID and user.intUserID != payload.user_id:
                    user.AddOpdut()
                elif user.strUserID == authorID and user.intUserID == payload.user_id:
                    user.removeOpdut()
                    user.removeOpdut()

        elif payload.emoji.id == kurtDisapproved:
            message = await client.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            authorDict = message["author"]
            authorID = authorDict["id"] # String

            for user in users:
                if user.strUserID == authorID:
                    user.AddNeddut()

@client.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == 619105859615719434:
        if payload.emoji.id == kurtApproved:
            message = await client.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            authorDict = message["author"]
            authorID = authorDict["id"] # String

            for user in users:
                if user.strUserID == authorID and user.intUserID != payload.user_id:
                    user.removeOpdut()
                elif user.strUserID == authorID and user.intUserID == payload.user_id:
                    user.AddOpdut()
                    user.AddOpdut()

        elif payload.emoji.id == kurtDisapproved:
            message = await client.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            authorDict = message["author"]
            authorID = authorDict["id"] # String

            for user in users:
                if user.strUserID == authorID:
                    user.removeNeddut()

@client.event
async def on_message(message):
    if message.content == "!karma":
        for user in users:
            if message.author.id == user.intUserID:
                x = Db.mycol.find_one({ "Name": user.name })
                await message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]))


    # No checks at the moment, so will likely break with wrong inputs from user.
    if "!pomodoro" in message.content:
        # Maybe if user is certain role on discord, so not everyone can fuck with this.

        # This entire part is coded based on Kurts saying, I wish this was here.
        #x = message.content
        #string_pomodoro_time = x[10:]
        #string_break_time = x[-2:]
        #pomodoro_time = int(string_pomodoro_time)
        #break_time = int(string_break_time)
        #Pomodoro.startPomodoro(pomodoro_time, break_time)
        #t = Pomodoro.PomodoroTimer(10,Pomodoro.printer())
        #t.start()

        #timerThread = threading.Thread(target = test_method())
        #timerThread.start()
        t = threading.Timer(15.0, test_method())
        t.start()



    # Hidden easter egg for the boys
    if message.content == "!bot":
        await message.channel.send('Botten er så tæt på at være færdig :pinching_hand:')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for document in Db.mycol.find():
        print(document)


def test_method():
    print("TEST")
    time.sleep(1)
    

client.run(os.getenv("TOKEN"))