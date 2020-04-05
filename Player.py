import discord, Constants

async def play(message):
    if "latex" in message.content:
        channel = message.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable=Constants.DEFAULT_PLAYER_PATH, source="C:/Users/Sren/Documents/GitHub/DiscordKarmaBot/mp3-files/LatexBusters.mp3"))
        while vc.is_connected():
            if not vc.is_playing():
                await vc.disconnect()
    elif "bamse" in message.content:
        channel = message.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable=Constants.DEFAULT_PLAYER_PATH, source="C:/Users/Sren/Documents/GitHub/DiscordKarmaBot/mp3-files/test.mp3"))
        while vc.is_connected():
            if not vc.is_playing():
                await vc.disconnect()
    elif "inspiration" in message.content:
        channel = message.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable=Constants.DEFAULT_PLAYER_PATH, source="C:/Users/Sren/Documents/GitHub/DiscordKarmaBot/mp3-files/Ole_Wedel.mp3"))
        while vc.is_connected():
            if not vc.is_playing():
                await vc.disconnect()

async def playTimerEnd(channel):
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(executable=Constants.DEFAULT_PLAYER_PATH, source="C:/Users/Sren/Documents/GitHub/DiscordKarmaBot/mp3-files/test.mp3"))
    while vc.is_connected():
        if not vc.is_playing():
            await vc.disconnect()