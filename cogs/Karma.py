import discord
from discord.ext import commands
import Db
import models

class Karma(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.configuration = bot.get_cog("Configuration")

        # Emotes
        # Perhabs these should be moved into the configuration aswell ?
        self.kurt_approved = 619818932475527210
        self.kurt_disapproved = 651028634945060864
        self.meme_channel = 619105859615719434

    @commands.Cog.listener()
    async def on_ready(self):
        print("Karma cog is loaded")

    @commands.command(brief="i.e. .karma Hjorth")
    async def karma(self, ctx, *, name=None):
        user = self._karma(name, ctx.message.author.id)
        await ctx.send(
            f"{user.name} has {user.up_votes - user.down_votes} total karma. {user.up_votes} opdutter and {user.down_votes} neddutter",
            delete_after=self.configuration.short_delete_after_time)

    @staticmethod
    def _karma(name=str or None, _id=None):
        if name is None:
            return Db.get_user_by_id(_id)
        else:
            name = str(name).capitalize()
            return Db.get_user_by_name(name)

    @commands.command(brief="Returns all karma data from the database")
    async def leaderboard(self, ctx):
        embed = self._leaderboard()
        await ctx.send(embed=embed, delete_after=self.configuration.very_long_delete_after_time)

    @staticmethod
    def _leaderboard():
        amount = 6
        users = Db.get_amount_of_users(amount)
        embed = discord.Embed(title="The karma standings! :o)")
        for i in range(amount):
            embed.add_field(name=f'**{users[i].name}**',
                            value=f'> Total: {users[i].up_votes - users[i].down_votes}\n '
                                  f'> Opdutter: {users[i].up_votes}\n '
                                  f'> Neddutter: {users[i].down_votes}\n')
        return embed

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == self.meme_channel:
            if payload.emoji.id == self.kurt_approved:
                author_id = await self._get_author_id(payload.channel_id, payload.message_id)
                if int(author_id) == payload.user_id:
                    Db.update_user_up_votes(author_id, -2)
                else:
                    Db.update_user_up_votes(author_id, 1)
                await self._update_highest_opdut()
            elif payload.emoji.id == self.kurt_disapproved:
                author_id = await self._get_author_id(payload.channel_id, payload.message_id)
                Db.update_user_down_votes(author_id, 1)
                await self._update_highest_neddut()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id == self.meme_channel:
            if payload.emoji.id == self.kurt_approved:
                author_id = await self._get_author_id(payload.channel_id, payload.message_id)
                if int(author_id) == payload.user_id:
                    Db.update_user_up_votes(author_id, 2)
                else:
                    Db.update_user_up_votes(author_id, -1)
                await self._update_highest_opdut()
            elif payload.emoji.id == self.kurt_disapproved:
                author_id = await self._get_author_id(payload.channel_id, payload.message_id)
                Db.update_user_down_votes(author_id, -1)
                await self._update_highest_neddut()

    async def _get_author_id(self, channel_id, message_id):
        message = await self.bot.http.get_message(channel_id, message_id)  # Dictionary
        authorDict = message["author"]
        return authorDict["id"]  # String

    # Could perhabs enter into the reason who was overthrown in these two functions.
    async def _update_highest_opdut(self):
        most_up_votes_in_db = Db.get_highest_up_votes()
        guild = self.bot.get_guild(self.configuration.guild_id)
        role = guild.get_role(self.configuration.most_up_votes_role_id)
        current_leader_on_discord = role.members[0].id
        if current_leader_on_discord != most_up_votes_in_db:
            await role.members[0].remove_roles(role, reason=f'Overthrown for most opduts')
            new_leader = guild.get_member(most_up_votes_in_db)
            await new_leader.add_roles(role, reason=f'Overthrew the old leader for most opduts')

    async def _update_highest_neddut(self):
        most_down_votes_in_db = Db.get_highest_down_votes()
        guild = self.bot.get_guild(self.configuration.guild_id)
        role = guild.get_role(self.configuration.most_up_votes_role_id)
        current_leader_on_discord = role.members[0].id
        if current_leader_on_discord != most_down_votes_in_db:
            await role.members[0].remove_roles(role, reason='Overthrown for most nedduts')
            new_leader = guild.get_member(most_down_votes_in_db)
            await new_leader.add_roles(role, reason='Overthrew the old leader for most nedduts')


def setup(bot):
    bot.add_cog(Karma(bot))
