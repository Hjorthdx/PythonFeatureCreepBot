import discord
from discord.ext import commands
import sys
sys.path.insert(0,"C:/Users/Sren/Documents/GitHub/DiscordKarmaBot")
import Db, User #pylint: disable=import-error


class Karma(commands.Cog):
    # Some documentation
    
    def __init__(self, bot):
        self.bot = bot

        # Emotes
        self.kurtApproved = 619818932475527210
        self.kurtDisapproved = 651028634945060864
        self.migmigChannel = 619105859615719434

        # Instantiating all the users
        Adil = User.User('Adil', 100552145421467648, '100552145421467648')
        Chrille = User.User('Chrille', 279307446009462784, '279307446009462784')
        Hjorth = User.User('Hjorth', 140195461519769601, '140195461519769601')
        Martin = User.User('Martin', 103033943464353792, '502882469721407509')
        Magnus = User.User('Magnus', 272507977984901120, '272507977984901120')
        Simon = User.User('Simon', 619105357473775636, '619105357473775636')
        self.users = [
            Adil,
            Chrille,
            Hjorth,
            Martin,
            Magnus,
            Simon
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Karma cog is loaded")  

    @commands.command(help="i.e. !karma Hjorth")
    async def karma(self, ctx):
        if ctx.message.content == "!karma":
            for user in self.users:
                if ctx.message.author.id == user.intUserID:
                    x = Db.mycol.find_one({ "Name": user.name })
                    await ctx.message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]), delete_after=15)
        else:
            for user in self.users:
                if user.name in ctx.message.content:
                    x = Db.mycol.find_one({ "Name": user.name })
                    await ctx.message.channel.send('{} has {} total karma. {} opdutter and {} neddutter'.format(x["Name"], x["Opdutter"] - x["Neddutter"], x["Opdutter"], x["Neddutter"]), delete_after=15)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == self.migmigChannel: 
            if payload.emoji.id == self.kurtApproved:
                message = await self.bot.http.get_message(payload.channel_id, payload.message_id) # Dictionary
                authorDict = message["author"]
                authorID = authorDict["id"] # String

                for user in self.users:
                    if user.strUserID == authorID and user.intUserID != payload.user_id:
                        user.AddOpdut()
                    elif user.strUserID == authorID and user.intUserID == payload.user_id:
                        user.removeOpdut()
                        user.removeOpdut()

            elif payload.emoji.id == self.kurtDisapproved:
                message = await self.bot.http.get_message(payload.channel_id, payload.message_id) # Dictionary
                authorDict = message["author"]
                authorID = authorDict["id"] # String

                for user in self.users:
                    if user.strUserID == authorID:
                        user.AddNeddut()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id == self.migmigChannel:
            if payload.emoji.id == self.kurtApproved:
                message = await self.bot.http.get_message(payload.channel_id, payload.message_id) # Dictionary
                authorDict = message["author"]
                authorID = authorDict["id"] # String

                for user in self.users:
                    if user.strUserID == authorID and user.intUserID != payload.user_id:
                        user.removeOpdut()
                    elif user.strUserID == authorID and user.intUserID == payload.user_id:
                        user.AddOpdut()
                        user.AddOpdut()

            elif payload.emoji.id == self.kurtDisapproved:
                message = await self.bot.http.get_message(payload.channel_id, payload.message_id) # Dictionary
                authorDict = message["author"]
                authorID = authorDict["id"] # String

                for user in self.users:
                    if user.strUserID == authorID:
                        user.removeNeddut()

def setup(bot):
    bot.add_cog(Karma(bot))