import discord
from discord.ext import commands


class Configuration(commands.Cog):
    # Some documentation
    # This is where all "constants" are placed.
    # Since they are not constant they are placed in this cog,
    # as it can then be reloaded on run time.
    # This should change the delete after time for all the other commands without having to restart the bot.

    def __init__(self, bot):
        self.bot = bot
        self.short_delete_after_time = 15
        self.medium_delete_after_time = 30
        self.long_delete_after_time = 60
        self.very_long_delete_after_time = 600
        self.guild_id = 619094316106907658
        self.most_up_votes_role_id = 762306236845916231
        self.most_down_votes_role_id = 762319929521209345

    @commands.Cog.listener()
    async def on_ready(self):
        print("Configuration cog is loaded")

    def test_func(self):
        return True


def setup(bot):
    bot.add_cog(Configuration(bot))
