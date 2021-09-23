import discord, os
from discord.ext import commands


class Configuration(commands.Cog):
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
        self.mp3_folder_path = "C:/Users/Sren/PycharmProjects/DiscordFeatureCreepBot/mp3-files/"
        self.gifs_folder_path = "C:/Users/Sren/PycharmProjects/DiscordFeatureCreepBot/gifs/"
        self.schedule_check_API_LINK = os.getenv("SCHEDULE_CHECK_API")
        self.timeout_time = 60

        # P7
        self.p7_generel_room_id = 885155224489197573
        self.p7_category_id = 630796890182516737

    @commands.Cog.listener()
    async def on_ready(self):
        print("Configuration cog is loaded")

    def test_func(self):
        return True


def setup(bot):
    bot.add_cog(Configuration(bot))
