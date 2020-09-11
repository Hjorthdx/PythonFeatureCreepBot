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

    @commands.command(brief="!play slet dem. !available for list of all mp3's.")
    async def play(self, ctx):
        if "latex" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Latex.mp3")
        elif "help" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Help.mp3")
        elif "honor" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Honor.mp3")
        elif "bamse" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Bamse.mp3")
        elif "inspiration" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Inspiration.mp3")
        elif "danger" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Danger.mp3")
        elif "worst day" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Worst day.mp3")
        elif "HA" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "HA.mp3")
        elif "shit" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Shit.mp3")
        elif "autism" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Autism.mp3")
        elif "loud" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Loud.mp3")
        elif "top10" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Top10.mp3")
        elif "mission failed" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Mission failed.mp3")
        elif "big smoke" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Big smoke.mp3")
        elif "slet dem" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Slet dem.mp3")
        elif "lyt nu" in ctx.message.content:
            channel = ctx.message.author.voice.channel
            await self.joinAndPlay(channel, self.basePath + "Lyt nu.mp3")
        await ctx.message.delete()

    async def joinAndPlay(self, channel, mp3):
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe", source=mp3))
        while vc.is_connected():
            if not vc.is_playing():
                await vc.disconnect()

    @commands.command(help="Shows all the current mp3 files")
    async def available(self, ctx):
        availableMp3Files = "```"
        for filename in os.listdir('./DiscordKarmaBot/mp3-files'):
            if filename.endswith('.mp3'):
                availableMp3Files += f"{filename[:-4]}\n"
        availableMp3Files+="```"
        await ctx.send(availableMp3Files, delete_after=15)

    @commands.command(help="Command for the Pomodoro cog to utilize", self_bot=True, hidden=True)
    async def PlayPomodoro(self, ctx):
        channel = ctx.message.author.voice.channel
        await self.joinAndPlay(channel, self.basePath + "Lyt nu.mp3")

def setup(bot):
    bot.add_cog(Player(bot))