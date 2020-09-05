import os, discord, pymongo, User, Db, time, Pomodoro, Constants, Player, requests
from dotenv import load_dotenv
from youtube_dl import YoutubeDL
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
    if message.author != client.user:
        if "!karma" in message.content:
            if message.content == "!karma":
                for user in users:
                    if message.author.id == user.intUserID:
                        x = Db.mycol.find_one({ "Name": user.name })
                        await message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]), delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
            else:
                for user in users:
                    if user.name in message.content:
                        x = Db.mycol.find_one({ "Name": user.name })
                        await message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]), delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
            await message.delete()           

        if "!pomodoro" in message.content:
            await Pomodoro.startTimers(message)
            await message.delete()

        if "!time" in message.content:
            await message.channel.send('Remaining time: {}'.format(Pomodoro.calculateRemainingTime()), delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
            await message.delete()

        if "!changeDefault" in message.content:
            x = [int(s) for s in message.content.split() if s.isdigit()]
            if "work" in message.content:
                Constants.DEFAULT_WORKTIME = x[0]
            elif "break" in message.content:
                Constants.DEFAULT_BREAKTIME = x[0]
            await message.delete()

        if "!p" in message.content:
            await Player.play(message)
            await message.delete()

        if "!yt" in message.content:
            channel = message.author.voice.channel
            url = message.content.strip("!yt ")
            song_there = os.path.isfile("youtube.mp3")

            try:
                if song_there:
                    os.remove("youtube.mp3")
            except PermissionError:
                print("Error")

            ydl_opts = {
                'verbose': True,
                'format': 'bestaudio/best', # choice of quality
                'outtmpl': 'youtube.%(ext)s',  # name the location
                'noplaylist' : True,        # only download single song, not playlist
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("Downloaded")
            await Player.joinAndPlay(channel, Constants.DEFAULT_YOUTUBE_LINK)
            print("Playing")
            await message.delete()

        if message.content == "!help":
            await message.channel.send("Current commands: \n * !karma - !karma Hjorth e.g. \n * !pomodoro - Default timers. !pomodoro 50 10 e.g. for 50/10 timer \n * !time - Remaining time on pomodoro \n * !changeDefault - !changeDefault work 50 e.g. \n * !p - Currently latex, bamse, inspiration, worst day, HA, shit, autism, loud, top10, help me, honor, mission failed. !p latex e.g. \n * !bot - Bot snart færdig meme \n * !trello - Trello link \n * !rapport - Rapport link \n * !watch - Followed by youtube link \n", delete_after=Constants.DEFAULT_DELETE_WAIT_TIME*3)
            await message.delete()
        
        if message.content == "!bot":
            await message.channel.send('Botten er så tæt på at være færdig :pinching_hand:', delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
            await message.delete()
        
        if message.content == "!trello":
            await message.channel.send(Constants.TRELLO_LINK, delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
            await message.delete()
        
        if message.content == "!rapport":
            await message.channel.send(Constants.RAPPORT_LINK, delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
            await message.delete()

        if "!watch" in message.content:
            url = message.content
            url.replace("!watch", "")
            await message.delete()
            x = generateWatch2getherURL(url)
            await message.channel.send(x, delete_after=Constants.DEFAULT_DELETE_WAIT_TIME * 3)
            


        #if "!w begin" in message.content:
            #x = await message.channel.send("React to this message to join") # Delete after !stop called
            #x.channel.react(kurtApproved)
            
            #newRun = WikiSpeedrun.Speedrun(WIKIPEDIA_RANDOM_LINK, endUrl)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for document in Db.mycol.find():
        print(document)

def generateWatch2getherURL(request):
    obj = {'share': request, 'api_key': Constants.API_KEY}
    x = requests.post(Constants.WATCH2GETHER_BASELINK, data=obj)
    y = x.json()
    streamkey = y['streamkey']
    return Constants.WATCH2GETHER_ROOMLINK + streamkey

client.run(os.getenv("TOKEN"))
