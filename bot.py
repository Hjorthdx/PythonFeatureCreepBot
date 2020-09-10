import os, discord, pymongo, User, Db, time, Constants
from dotenv import load_dotenv
from youtube_dl import YoutubeDL
from discord.ext import commands
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

bot = commands.Bot(command_prefix='!')

@bot.command(help="i.e. !karma Hjorth")
async def karma(ctx):
    if ctx.message.content == "!karma":
        for user in users:
            if ctx.message.author.id == user.intUserID:
                x = Db.mycol.find_one({ "Name": user.name })
                await ctx.message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]), delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
    else:
        for user in users:
            if user.name in ctx.message.content:
                x = Db.mycol.find_one({ "Name": user.name })
                await ctx.message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]), delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
    await ctx.message.delete()  

@bot.command(help="!changeDefault work 50 e.g.")
async def changeDefault(ctx):
    x = [int(s) for s in ctx.message.content.split() if s.isdigit()]
    if "work" in ctx.message.content:
        Constants.DEFAULT_WORKTIME = x[0]
    elif "break" in ctx.message.content:
        Constants.DEFAULT_BREAKTIME = x[0]
    await ctx.message.delete()

@bot.command(help="Trello link")
async def trello(ctx):
    await ctx.message.channel.send(Constants.TRELLO_LINK, delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
    await ctx.message.delete()

@bot.command(help="Rapport link")
async def rapport(ctx):
    await ctx.message.channel.send(Constants.RAPPORT_LINK, delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
    await ctx.message.delete()

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 619105859615719434: 
        if payload.emoji.id == kurtApproved:
            message = await bot.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            authorDict = message["author"]
            authorID = authorDict["id"] # String

            for user in users:
                if user.strUserID == authorID and user.intUserID != payload.user_id:
                    user.AddOpdut()
                elif user.strUserID == authorID and user.intUserID == payload.user_id:
                    user.removeOpdut()
                    user.removeOpdut()

        elif payload.emoji.id == kurtDisapproved:
            message = await bot.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            authorDict = message["author"]
            authorID = authorDict["id"] # String

            for user in users:
                if user.strUserID == authorID:
                    user.AddNeddut()

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == 619105859615719434:
        if payload.emoji.id == kurtApproved:
            message = await bot.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            authorDict = message["author"]
            authorID = authorDict["id"] # String

            for user in users:
                if user.strUserID == authorID and user.intUserID != payload.user_id:
                    user.removeOpdut()
                elif user.strUserID == authorID and user.intUserID == payload.user_id:
                    user.AddOpdut()
                    user.AddOpdut()

        elif payload.emoji.id == kurtDisapproved:
            message = await bot.http.get_message(payload.channel_id, payload.message_id) # Dictionary
            authorDict = message["author"]
            authorID = authorDict["id"] # String

            for user in users:
                if user.strUserID == authorID:
                    user.removeNeddut()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    for document in Db.mycol.find():
        print(document)    

@bot.command(hidden=True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.message.delete()

@bot.command(hidden=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.message.delete()

for filename in os.listdir('./DiscordKarmaBot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
    

bot.run(os.getenv("TOKEN"))
