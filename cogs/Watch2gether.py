import discord
import requests
import os
from discord.ext import commands


class Watch2gether(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.watch2gether_baselink = "https://w2g.tv/rooms/create.json"
        self.watch2gether_roomlink = "https://w2g.tv/rooms/"
        self.API_key = os.getenv("WATCH2GETHER_APIKEY")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Watch2gether cog is loaded")

    @commands.command(
        help="Creates a watch2gether room and automatically inserts the linked youtube video.",
        brief="returns watch2gether room with youtube video", aliases=['w2g', 'watch2gether'])
    async def watch(self, ctx):
        url = ctx.message.content.replace("!watch", "")
        await ctx.message.delete()
        x = self.generate_watch2gether_url(url)
        await ctx.message.channel.send(x, delete_after=15)

    def generate_watch2gether_url(self, request):
        obj = {'share': request, 'api_key': self.API_key}
        x = requests.post(self.watch2gether_baselink, data=obj)
        y = x.json()
        stream_key = y['streamkey']
        return self.watch2gether_roomlink + stream_key


def setup(bot):
    bot.add_cog(Watch2gether(bot))
