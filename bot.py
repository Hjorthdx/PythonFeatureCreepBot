import os
import discord
import asyncio
import pymongo


# THINGS TO REMEMBER
# <:kurtApproved:619818932475527210>
# <:kurtDisapproved:651028634945060864>

# BUGS TO FIX
# User can just remove reaction and then react again
# to completely manipulate karma on the server.


# Discord bot token
TOKEN = 'NjkwNTM0MDI4MzE0NjczMTUy.XnS0Gw.C7h7bJETMXueU8WHv2saMqT44JQ'


# Connects to mongo db @ localhost
# Creates a database and collection with assigned names,
# if they do not already exist in the database.
myClient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myClient["mydatabase"]
mycol = mydb["UserKarma"]


# Checks if there is any documents in the database,
# If there isn't, then it adds all the users and print their ids.
if mycol.find():
    # Do nothing
    print('Found documents')
else:
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

client = discord.Client()

# Needs to a discord.utily.find to find the message.
# Once the message is found determine the user and call
# the add karma function that isnt implemented yet.
@client.event
async def on_raw_reaction_add(payload):
    # Is it migmig room ?
    if payload.channel_id == 619105859615719434:
        # Kurt approved
        if payload.emoji.id == 619818932475527210:
            print("Kurt approved found, +1 opdut")
        # Kurt disapproved
        elif payload.emoji.id == 651028634945060864:
            print("Kurt disapproved found, +1 neddut")



@client.event
async def on_message(message):
    print(message)
    # Hidden easter egg for the boys
    if message.channel != 690538239433506816 and message.author != client.user and message.content == "!karma":
        await message.channel.send('Botten er så tæt på at være færdig :pinching_hand:')
    # SØREN
    if message.author.id == 140195461519769601:
        mycol.update_one(
            { "Name": "Hjorth" },
            { "$inc": {"Opdutter": 1}}
        )
        x = mycol.find_one({"Name": "Hjorth"})
        print(x)
        # await message.channel.send('Hjorth texted')
        print("KARMA ADDED TO HJORTH")
    # CHRILLE
    elif message.author.id == 279307446009462784:
        #karmaDict['Chrille'] += 1
        print("KARMA ADDED TO CHRILLE")
    # LØNNE
    elif message.author.id == 103033943464353792:
        #karmaDict['Martin'] += 1
        print("KARMA ADDED TO LØNNE")
    # MAGNUS
    elif message.author.id == 272507977984901120:
        #karmaDict['Magnus'] += 1
        print("KARMA ADDED TO MAGNUS")
    # SIMON
    elif message.author.id == 619094316106907658:
        #karmaDict['Simon'] += 1
        print("KARMA ADDED TO SIMON")
    
    ## MANGLER STEN OG ADIL

# When the bot succesfully joins the discord server.
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for document in mycol.find():
        print(document)

client.run(TOKEN)