import discord
import requests
import os
from discord.ext import commands


class Watch2gether(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.configuration = bot.get_cog("Configuration")
        self.watch2gether_baselink = "https://w2g.tv/rooms/create.json"
        self.watch2gether_roomlink = "https://w2g.tv/rooms/"
        self.API_key = os.getenv("WATCH2GETHER_APIKEY")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Watch2gether cog is loaded")

    @commands.command(help="Creates a watch2gether room and automatically inserts the linked youtube video.",
                      brief="returns watch2gether room with youtube video", aliases=['w2g', 'watch2gether'])
    async def watch(self, ctx, url):
        watch2gether_url = self._generate_watch2gether_url(url)
        await ctx.message.channel.send(watch2gether_url, delete_after=self.configuration.very_long_delete_after_time)

    def _generate_watch2gether_url(self, request):
        data = {'share': request, 'api_key': self.API_key}
        response = requests.post(self.watch2gether_baselink, data=data)
        response_json = response.json()
        stream_key = response_json['streamkey']
        return self.watch2gether_roomlink + stream_key


def setup(bot):
    bot.add_cog(Watch2gether(bot))
