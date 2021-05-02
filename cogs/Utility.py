import discord
from discord.ext import commands


class Utility(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.configuration = bot.get_cog("Configuration")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility cog is loaded")

    @commands.command(name="save_all")
    @commands.is_owner()
    async def save_all_message_attachments_from_channel(self, ctx, channel_id=None):
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            await ctx.send("Channel is none. Please check if channel id is correct",
                           delete_after=self.configuration.short_delete_after_time)
        messages = await channel.history(limit=None).flatten()
        print(len(messages))
        for message in messages:
            if message.attachments is not None:
                for attachment in message.attachments:
                    if self._is_wanted_file_type(attachment.filename):
                        print(f'id: {message.author.display_name}, filename: {attachment.filename}')
                        await attachment.save(str(message.author.display_name) + str(attachment.id) + attachment.filename)

# Flet de her to sammen så det bliver et stort monster og så kan jeg døje med det senere.
    '''
    async def get_all_memes_from_migmig_channel_that_has_remouladeklat_or_opdut():
        channel = bot.get_channel(619105859615719434)
        messages = await channel.history(limit=None).flatten()
        print(len(messages))
        for message in messages:
            if message.reactions is not None:
                if message.attachments is not None:
                    for reaction in message.reactions:
                        try:
                            if reaction.emoji.id == 619818932475527210 or reaction.emoji.id == 619197419137007644:
                                for attachment in message.attachments:
                                    print(f'id: {message.author.display_name}, filename: {attachment.filename}')
                                    await attachment.save(str(reaction.count) + str(message.author.display_name) + str(
                                        attachment.id) + attachment.filename)
                        except AttributeError as e:
                            print(f'{e}, message author: {message.author.display_name}')
    '''
    @staticmethod
    def _is_wanted_file_type(filename):
        if filename.endswith('.png') or filename.endswith('.jpg') or \
                filename.endswith('.mp3') or filename.endswith('.mp4'):
            return True
        else:
            return False


def setup(bot):
    bot.add_cog(Utility(bot))
