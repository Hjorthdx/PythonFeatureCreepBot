import discord, Constants

async def play(message):
    if "latex" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.LATEXBUSTERS)
    elif "bamse" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.BAMSE)
    elif "inspiration" in message.content:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.OLE)
    else:
        channel = message.author.voice.channel
        await joinAndPlay(channel, Constants.BAMSE)

async def playTimerEnd(channel):
    await joinAndPlay(channel, Constants.OLE)

async def joinAndPlay(channel, mp3):
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(executable=Constants.DEFAULT_PLAYER_PATH, source=mp3))
    while vc.is_connected():
        if not vc.is_playing():
            await vc.disconnect()