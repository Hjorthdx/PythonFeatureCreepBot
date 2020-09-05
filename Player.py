import discord, Constants
from youtube_dl import YoutubeDL


async def play(message, timerBool=None):
    if "latex" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.LATEXBUSTERS)
    elif "help" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.HELP_ME_HELP_YOU)
    elif "honor" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.HONOR)
    elif "bamse" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.BAMSE)
    elif "inspiration" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.OLE)
    elif "danger" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.DANGER)
    elif "worst day" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.WORSTDAY)
    elif "HA" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.HA)
    elif "shit" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.SHIT)
    elif "autism" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.AUTISM)
    elif "loud" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.LOUD)
    elif "top10" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.TOP10)
    elif "mission failed" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.MISSION_FAILED)
    elif "big smoke" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.BIG_SMOKE_FOOD_ORDER)
    elif "slet dem" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.SLET_DEM)
    elif "lyt nu" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.LYT_NU)
    elif "youtubefile" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, "C:/Users/Sren/Documents/GitHub/youtube.mp3")
    elif timerBool == True:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.BAMSE)

async def joinAndPlay(channel, mp3):
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(executable=Constants.DEFAULT_PLAYER_PATH, source=mp3))
    while vc.is_connected():
        if not vc.is_playing():
            await vc.disconnect()

def downloadYoutube(url):
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

    #ydl = YoutubeDL(ydl_opts)
    #ydl.download([url])
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])