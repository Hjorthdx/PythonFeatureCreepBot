import discord
from discord.ext import commands


class Configuration(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.short_delete_after_time = 15
        self.medium_delete_after_time = 30
        self.long_delete_after_time = 60
        self.very_long_delete_after_time = 600

    @commands.Cog.listener()
    async def on_ready(self):
        print("Configuration cog is loaded")


def setup(bot):
    bot.add_cog(Configuration(bot))
