import os, discord, pymongo, User, Db, threading, time, Pomodoro
from dotenv import load_dotenv


load_dotenv()

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

    if "!pomodoro" in message.content:
        Pomodoro.startTimer(message)

    if "!latex" in message.content:
        channel = message.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe", source="C:/Users/Sren/Documents/GitHub/DiscordKarmaBot/mp3-files/LatexBusters.mp3"))
        while vc.is_connected():
            if not vc.is_playing():
                await vc.disconnect()

    if "!play" in message.content:
        if message.author.bot:
            channel = client.get_channel(619094316106907662)
        else:
            channel = message.author.voice.channel
        
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe", source="C:/Users/Sren/Documents/GitHub/DiscordKarmaBot/mp3-files/test.mp3"))
        while vc.is_connected():
            if not vc.is_playing():
                await vc.disconnect()

    if "!inspiration" in message.content:
        channel = message.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe", source="C:/Users/Sren/Documents/GitHub/DiscordKarmaBot/mp3-files/Ole_Wedel.mp3"))
        while vc.is_connected():
            if not vc.is_playing():
                await vc.disconnect()

    # Hidden easter egg for the boys
    if message.content == "!bot":
        await message.channel.send('Botten er så tæt på at være færdig :pinching_hand:')

# Lav fil med metode der gør alt det der spiller lyd. Abstraher alt det lort væk

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for document in Db.mycol.find():
        print(document)

client.run(os.getenv("TOKEN"))
