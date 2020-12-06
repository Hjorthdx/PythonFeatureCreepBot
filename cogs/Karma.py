import discord
from discord.ext import commands
import Db

# ctx.message.guild ? Will this fix the role.members returning an empty list. Not sure. Perhabs karma class can have this guild saved as field
class Karma(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot

        # Emotes
        self.kurtApproved = 619818932475527210
        self.kurtDisapproved = 651028634945060864
        self.migmigChannel = 619105859615719434

    @commands.Cog.listener()
    async def on_ready(self):
        print("Karma cog is loaded")

    @commands.command(brief="i.e. .karma Hjorth")
    async def karma(self, ctx, *, name: str or None):
        print(name)
        if name is None:
            author_id = ctx.message.author.id
            query = f"SELECT * FROM users WHERE id={author_id}"
            print(query)
            x = await Db.myfetch(query)
            print(x)
            await ctx.send(f"{x[0][1]} has {x[0][2] - x[0][3]} total karma. {x[0][2]} opdutter and {x[0][3]} neddutter", delete_after=15)
        elif name is not None:
            query = f"SELECT * FROM users WHERE name='{name}'"
            print(query)
            x = await Db.myfetch(query)
            print(x)
            await ctx.send(f"{x[0][1]} has {x[0][2] - x[0][3]} total karma. {x[0][2]} opdutter and {x[0][3]} neddutter", delete_after=15)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == self.migmigChannel:
            if payload.emoji.id == self.kurtApproved:
                message = await self.bot.http.get_message(payload.channel_id, payload.message_id) # Dictionary
                authorDict = message["author"]
                author_id = authorDict["id"] # String

                if int(author_id) == payload.user_id:
                    print("Self opdut :o)")
                    # Perhabs karma cog shouldnt know about this
                    # Should just call db method and say the amount e.g. - 2 and the author id
                    query = "UPDATE users SET opdutter = opdutter - 2 WHERE id=" + author_id
                    await Db.myfetch(query)
                elif author_id != payload.user_id:
                    query = "UPDATE users SET opdutter = opdutter + 1 WHERE id=" + author_id
                    await Db.myfetch(query)
                await self.update_highest_opdut()

            elif payload.emoji.id == self.kurtDisapproved:
                message = await self.bot.http.get_message(payload.channel_id, payload.message_id)  # Dictionary
                authorDict = message["author"]
                author_id = authorDict["id"]  # String
                query = "UPDATE users SET opdutter = neddutter + 1 WHERE id=" + author_id
                await Db.myfetch(query)
                await self.update_highest_neddut()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id == self.migmigChannel:
            if payload.emoji.id == self.kurtApproved:
                message = await self.bot.http.get_message(payload.channel_id, payload.message_id) # Dictionary
                authorDict = message["author"]
                author_id = authorDict["id"] # String

                if int(author_id) == payload.user_id:
                    query = "UPDATE users SET opdutter = opdutter + 2 WHERE id=" + author_id
                    await Db.myfetch(query)
                elif author_id != payload.user_id:
                    query = "UPDATE users SET opdutter = opdutter - 1 WHERE id=" + author_id
                    await Db.myfetch(query)
                await self.update_highest_opdut()

            elif payload.emoji.id == self.kurtDisapproved:
                message = await self.bot.http.get_message(payload.channel_id, payload.message_id)  # Dictionary
                authorDict = message["author"]
                author_id = authorDict["id"]  # String
                query = "UPDATE users SET opdutter = neddutter - 1 WHERE id=" + author_id
                await Db.myfetch(query)
                await self.update_highest_neddut()

    async def update_highest_opdut(self):
        highest_opdutted = await Db.myfetch(
            "SELECT id, name, opdutter FROM users ORDER BY opdutter DESC LIMIT 1;")
        print(highest_opdutted)
        guild = self.bot.get_guild(619094316106907658)
        role = guild.get_role(762306236845916231)
        current_leader = role.members[0].id
        print(highest_opdutted[0][1])
        if current_leader != highest_opdutted[0][0]:
            await role.members[0].remove_roles(role, reason='No longer most opduts')
            new_leader = guild.get_member(highest_opdutted[0][0])
            await new_leader.add_roles(role, reason='Most opduttet')
            print(f"New leader is {new_leader}")
        else:
            print("Same old leader")

    async def update_highest_neddut(self):
        highest_neddutted = await Db.myfetch(
            "SELECT id, name, neddutter FROM users ORDER BY neddutter DESC LIMIT 1;")
        print(highest_neddutted)
        guild = self.bot.get_guild(619094316106907658)
        role = guild.get_role(762319929521209345)
        current_leader = role.members[0].id
        print(highest_neddutted[0][0])
        if current_leader != highest_neddutted[0][0]:
            await role.members[0].remove_roles(role, reason='No longer most nedduts')
            new_leader = guild.get_member(highest_neddutted[0][0])
            await new_leader.add_roles(role, reason='Most nedduttet')
            print("New roles given")
        else:
            print("Same old leader")


def setup(bot):
    bot.add_cog(Karma(bot))
