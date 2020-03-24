# bot.py
import os
import discord
import asyncio
import pymongo

TOKEN = 'NjkwNTM0MDI4MzE0NjczMTUy.XnS0Gw.C7h7bJETMXueU8WHv2saMqT44JQ'

myClient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myClient["mydatabase"]
mycol = mydb["UserKarma"]

# Måske er et dictionary bedre for så kan jeg tilgå direkte til det element jeg gerne vil finde
# Bare ved at bruge keyword ( deres navn ), og så kan jeg opdatere værdien
# Jeg kan ikke helt lure hvordan jeg skulle gøre det nu, nu når jeg bare har et langt array.
# Men det er også sent, så måske virker min hjerne bare ikke mere.
karmaList = [
    {"Name": "Adil", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Chrille", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Hjorth", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Martin", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Magnus", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Simon", "Opdutter": 0, "Neddutter": 0},
    {"Name": "Sten", "Opdutter": 0, "Neddutter": 0}
]

karmaDict = {
    "Adil": 0,
    "Chrille": 0,
    "Hjorth": 0,
    "Martin": 0,
    "Magnus": 0,
    "Simon": 0,
    "Sten": 0
}

x = mycol.insert_many(karmaList)
print(x.inserted_ids)

client = discord.Client()

#async def update_karma():
    #await client.wait_until_ready()
    #while not client.is_closed():
    #    try:
     #       with open("karma.txt", "a") as f:
     #           for x, y in karmaDict.items():
     #               f.write(f"{x}: {y}\n")
     #       await asyncio.sleep(5) # Do 10 minutes later 600
    #    except Exception as e:
    #        print(e)

@client.event
async def on_message(message):
    print(message)

    # Hidden easter egg for the boys
    if message.channel != 690538239433506816 and message.author != client.user and message.content == "!karma":
        await message.channel.send('Botten er så tæt på at være færdig :pinching_hand:')

    # SØREN
    if message.author.id == 140195461519769601:
        #query = {"Name": {"Hjorth"}}
        #val = 0
        #new = {"$set": {"Opdutter": val}} # Last "" I need to figure out a way to ++ that bitch

        #x = mycol.update_one(query, new)

        x = mycol.find({}, {"Name": "Hjorth"})
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

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)