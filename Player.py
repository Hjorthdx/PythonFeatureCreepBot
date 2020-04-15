import discord, Constants

async def play(message=None, timerBool=None):
    if "latex" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.LATEXBUSTERS)
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
    elif timerBool == True:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.BAMSE)

async def joinAndPlay(channel, mp3):
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(executable=Constants.DEFAULT_PLAYER_PATH, source=mp3))
    while vc.is_connected():
        if not vc.is_playing():
            await vc.disconnect()