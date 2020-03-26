import os
import discord
import pymongo
import User
import Db

# TODO
# The enviorement file does not work either, so the bot token needs to be refreshed each time it is pushed to git
# Add pomodoro timer
# Add another collection in the database to track how long we are working for, just like lønnes ui in his 

# Discord bot token
TOKEN = 'NjkwNTM0MDI4MzE0NjczMTUy.XnzZBA.T6dNTt6mkHRr2kxLZXfFZUYBscc'

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
        
    # Hidden easter egg for the boys
    if message.content == "!bot":
        await message.channel.send('Botten er så tæt på at være færdig :pinching_hand:')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for document in Db.mycol.find():
        print(document)

client.run(TOKEN)