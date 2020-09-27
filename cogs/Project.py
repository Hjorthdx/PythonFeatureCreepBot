import discord
from discord.ext import commands

class Project(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Project cog is loaded")

    @commands.command(help="Trello link")
    async def trello(self, ctx):
        await ctx.message.channel.send("https://trello.com/b/iFsYL4QH/weight-completion", delete_after=15)
        await ctx.message.delete()

    @commands.command(help="Rapport link")
    async def rapport(self, ctx):
        await ctx.message.channel.send("https://www.overleaf.com/project/5f56101b9841ac000168e006", delete_after=15)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Project(bot))
