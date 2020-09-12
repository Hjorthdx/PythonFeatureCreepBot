import discord, os
from discord.ext import commands

class Player(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.basePath = "C:/Users/Sren/Documents/GitHub/DiscordKarmaBot/mp3-files/"

    @commands.Cog.listener()
    async def on_ready(self):
        print("Player cog is loaded")

    @commands.command(brief="!play slet dem. !available for list of all mp3's")
    async def play(self, ctx, *, userInput):
        mp3 = self.basePath + userInput + ".mp3"
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(mp3))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.message.delete()

    @commands.command(help="!yt youtube link")
    async def yt(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title), delete_after=player.duration)
        await ctx.message.delete()

    @commands.command(help="Shows all the current mp3 files")
    async def available(self, ctx):
        availableMp3Files = "```"
        for filename in os.listdir('./DiscordKarmaBot/mp3-files'):
            if filename.endswith('.mp3'):
                availableMp3Files += f"{filename[:-4]}\n"
        availableMp3Files+="```"
        await ctx.send(availableMp3Files, delete_after=15)

    @commands.command(brief="Changes the volume the bot is playing", help="I.e. !volume 60 sets the volume to 60%")
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume), delete_after=15)
        await ctx.message.delete()

    # Was the join command before. Just renamed for now until further notice with the wikipedia speedrun
    @commands.command(help="Makes the bot join a desired voice channel")
    async def connect(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        
        await channel.connect()
        await ctx.message.delete()

    @commands.command(help="Makes the bot leave voice channel")
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.message.delete()

    @play.before_invoke
    @yt.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @play.after_invoke
    @yt.after_invoke
    async def ensure_left_voice(self, ctx):
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

    @commands.command(help="Command for the Pomodoro cog to utilize", self_bot=True, hidden=True)
    async def PlayPomodoro(self, ctx):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.basePath + "Lyt nu.mp3"))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

def setup(bot):
    bot.add_cog(Player(bot))


import asyncio, youtube_dl

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)