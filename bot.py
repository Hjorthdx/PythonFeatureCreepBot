import os
import discord
import pymongo
import User

# TODO
# Update the methods add and remove opdut/neddut
# Update the on message so it utitilzes the classes
# The enviorement file does not work either, so the bot token needs to be refreshed each time it is pushed to git
# Add pomodoro timer
# Add another collection in the database to track how long we are working for, just like lønnes ui in his 

# Discord bot token
TOKEN = 'NjkwNTM0MDI4MzE0NjczMTUy.Xnywkw.3khS0bjR-O503PMviXnvHjrvY1I'

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

client = discord.Client()
"""
def addOpdut(authorID):
    # ADIL
    if authorID == '100552145421467648':
        mycol.update_one(
            { "Name": "Adil" },
            { "$inc": {"Opdutter": 1}}
        )
    # CHRILLE
    elif authorID == '279307446009462784':
        mycol.update_one(
            { "Name": "Chrille" },
            { "$inc": {"Opdutter": 1}}
        )
    # HJORTH
    elif authorID == '140195461519769601':
        mycol.update_one(
            { "Name": "Hjorth" },
            { "$inc": {"Opdutter": 1}}
        )
    # MARTIN
    elif authorID == '103033943464353792':
        mycol.update_one(
            { "Name": "Martin" },
            { "$inc": {"Opdutter": 1}}
        )
    # MAGNUS 
    elif authorID == '272507977984901120':
        mycol.update_one(
            { "Name": "Magnus" },
            { "$inc": {"Opdutter": 1}}
        )
    # SIMON 
    elif authorID == '619105357473775636':
        mycol.update_one(
            { "Name": "Simon" },
            { "$inc": {"Opdutter": 1}}
        )
    #STEN
    elif authorID == '502882469721407509':
        mycol.update_one(
            { "Name": "Sten" },
            { "$inc": {"Opdutter": 1}}
        )

def removeOpdut(authorID):
    # ADIL
    if authorID == '100552145421467648':
        mycol.update_one(
            { "Name": "Adil" },
            { "$inc": {"Opdutter": -1}}
        )
    # CHRILLE
    elif authorID == '279307446009462784':
        mycol.update_one(
            { "Name": "Chrille" },
            { "$inc": {"Opdutter": -1}}
        )
    # HJORTH
    elif authorID == '140195461519769601':
        mycol.update_one(
            { "Name": "Hjorth" },
            { "$inc": {"Opdutter": -1}}
        )
    # MARTIN
    elif authorID == '103033943464353792':
        mycol.update_one(
            { "Name": "Martin" },
            { "$inc": {"Opdutter": -1}}
        )
    # MAGNUS 
    elif authorID == '272507977984901120':
        mycol.update_one(
            { "Name": "Magnus" },
            { "$inc": {"Opdutter": -1}}
        )
    # SIMON
    elif authorID == '619094316106907658':
        mycol.update_one(
            { "Name": "Simon" },
            { "$inc": {"Opdutter": -1}}
        )
    #STEN
    elif authorID == '502882469721407509':
        mycol.update_one(
            { "Name": "Sten" },
            { "$inc": {"Opdutter": -1}}
        )

def addNeddut(authorID):
    # ADIL
    if authorID == '100552145421467648':
        mycol.update_one(
            { "Name": "Adil" },
            { "$inc": {"Neddutter": 1}}
        )
    # CHRILLE
    elif authorID == '279307446009462784':
        mycol.update_one(
            { "Name": "Chrille" },
            { "$inc": {"Neddutter": 1}}
        )
    # HJORTH
    elif authorID == '140195461519769601':
        mycol.update_one(
            { "Name": "Hjorth" },
            { "$inc": {"Neddutter": 1}}
        )
    # MARTIN
    elif authorID == '103033943464353792':
        mycol.update_one(
            { "Name": "Martin" },
            { "$inc": {"Neddutter": 1}}
        )
    # MAGNUS 
    elif authorID == '272507977984901120':
        mycol.update_one(
            { "Name": "Magnus" },
            { "$inc": {"Neddutter": 1}}
        )
    # SIMON 
    elif authorID == '619105357473775636':
        mycol.update_one(
            { "Name": "Simon" },
            { "$inc": {"Neddutter": 1}}
        )
    #STEN
    elif authorID == '502882469721407509':
        mycol.update_one(
            { "Name": "Sten" },
            { "$inc": {"Neddutter": 1}}
        )

def removeNeddut(authorID):
    # ADIL
    if authorID == '100552145421467648':
        mycol.update_one(
            { "Name": "Adil" },
            { "$inc": {"Neddutter": -1}}
        )
    # CHRILLE
    elif authorID == '279307446009462784':
        mycol.update_one(
            { "Name": "Chrille" },
            { "$inc": {"Neddutter": -1}}
        )
    # HJORTH
    elif authorID == '140195461519769601':
        mycol.update_one(
            { "Name": "Hjorth" },
            { "$inc": {"Neddutter": -1}}
        )
    # MARTIN
    elif authorID == '103033943464353792':
        mycol.update_one(
            { "Name": "Martin" },
            { "$inc": {"Neddutter": -1}}
        )
    # MAGNUS 
    elif authorID == '272507977984901120':
        mycol.update_one(
            { "Name": "Magnus" },
            { "$inc": {"Neddutter": -1}}
        )
    # SIMON 
    elif authorID == '619105357473775636':
        mycol.update_one(
            { "Name": "Simon" },
            { "$inc": {"Neddutter": -1}}
        )
    #STEN
    elif authorID == '502882469721407509':
        mycol.update_one(
            { "Name": "Sten" },
            { "$inc": {"Neddutter": -1}}
        )
"""
@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 619105859615719434:
        # Kurt approved  
        if payload.emoji.id == kurtApproved:
            message = await client.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            authorDict = message["author"]
            authorID = authorDict["id"] # String
            
            # If user upvotes his own post
            reactUserID = payload.user_id
            strUserID = str(reactUserID)
            if strUserID == authorID:
                removeOpdut(authorID)
                removeOpdut(authorID)
            else:
                addOpdut(authorID)
        # Kurt disapproved
        elif payload.emoji.id == kurtDisapproved:
            message = await client.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            authorDict = message["author"]
            authorID = authorDict["id"] # String
            addNeddut(authorID)

@client.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == 619105859615719434:
        # Kurt approved
        if payload.emoji.id == kurtApproved:
            message = await client.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            reactUserID = payload.user_id
            strUserID = str(reactUserID)
            authorDict = message["author"]
            authorID = authorDict["id"] # String

            # If user upvotes his own post
            if strUserID == authorID:
                addOpdut(authorID)
                addOpdut(authorID)
            else:
                removeOpdut(authorID)
        # Kurt disapproved
        elif payload.emoji.id == kurtDisapproved:
            message = await client.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            authorDict = message["author"]
            authorID = authorDict["id"] # String
            removeNeddut(authorID)

@client.event
async def on_message(message):
    if message.content == "!karma":
        # ADIL
        if message.author.id == Adil.intUserID:
            x = mycol.find_one({"Name": "Adil"})
            await message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]))
        # CHRILLE
        elif message.author.id == Chrille.intUserID:
            x = mycol.find_one({"Name": "Chrille"})
            await message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]))
        # HJORTH
        elif message.author.id == Hjorth.intUserID:
            x = mycol.find_one({"Name": "Hjorth"})
            await message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]))
        # MARTIN
        elif message.author.id == Martin.intUserID:
            x = mycol.find_one({"Name": "Martin"})
            await message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]))
        # MAGNUS 
        elif message.author.id == Magnus.intUserID:
            x = mycol.find_one({"Name": "Magnus"})
            await message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]))
        # SIMON
        elif message.author.id == Simon.intUserID:
            x = mycol.find_one({"Name": "Simon"})
            await message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]))
        #STEN
        elif message.author.id == Sten.intUserID:
            x = mycol.find_one({"Name": "Sten"})
            await message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]))

    # Hidden easter egg for the boys
    if message.content == "!bot":
        await message.channel.send('Botten er så tæt på at være færdig :pinching_hand:')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for document in mycol.find():
        print(document)

client.run(TOKEN)