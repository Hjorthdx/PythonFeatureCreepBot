import discord, datetime, wikipedia
from discord.ext import commands

class WikipediaSpeedrun(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.participants = []
        self.startingTime = None
        self.finishTime = None
        self.endArticle = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("WikipediaSpeedrun cog is loaded")

    @commands.command(help="Join the race")
    async def join(self, ctx):
        if ctx.message.author.display_name in self.participants:
            ctx.send("{}, you are already in the race! Stand by!".format(ctx.message.author.display_name), delete_after=15)
        else:
            self.participants.append(ctx.message.author.display_name)
        await ctx.send("{} joined the race! \n Current players are: \n{}".format(ctx.message.author.display_name, self.participants), delete_after=15)
        await ctx.message.delete()

    @commands.command(help="Leave the race")
    async def leave(self, ctx):
        if ctx.message.author.display_name not in self.participants:
            ctx.send("{}, you already not in the race!".format(ctx.message.author.display_name), delete_after=15)
        else:
            self.participants.remove(ctx.message.author.display_name)
        await ctx.send("{} left the race. \n Current players are: \n{}".format(ctx.message.author.display_name, self.participants), delete_after=15)
        await ctx.message.delete()

    @commands.command(brief="!goal article link", help="This is currently not saved, but it prob should be stored in the database, so we can keep score.")
    async def goal(self, ctx):
        if ctx.message.author.display_name in self.participants and self.endArticle == None:
            self.endArticle = ctx.message.content.replace("!goal", "")
            await ctx.send("The article to find is: {}".format(self.endArticle), delete_after=15)
        elif self.endArticle != None:
            await ctx.send("End article is already set! The goal is to find {}".format(self.endArticle), delete_after=15)
        elif ctx.message.author.display_name not in self.participants:
            await ctx.send("{}, you are not in the race. Join the race to set the goal".format(ctx.message.author.display_name), delete_after=15)
        await ctx.message.delete()

    @commands.command(brief="Starts the run", help="Atleast two competitors are needed to start a race.")
    async def start(self, ctx):
        if len(self.participants) == 0: #Should be more than 2? Who wants to race only themself, other than me while testing ofc.
            await ctx.send("Not enough competitors <:Spand:619148485379358739>", delete_after=15)
        else:
            await ctx.send("The race has begun!", delete_after=15)
            await ctx.send(wikipedia.page(wikipedia.random(1)).url, delete_after=15)
            self.startingTime = datetime.datetime.now()
        await ctx.message.delete()

    @commands.command(help="Ends the run and announces winner + elapsed time")
    async def done(self, ctx):
        if ctx.message.author.display_name in self.participants:
            self.finishTime = datetime.datetime.now()
            duration = self.finishTime - self.startingTime
            await ctx.send("{} is the winner! Finding the article in: {}".format(ctx.message.author.display_name, duration), delete_after=15) 
        else:
            await ctx.send("{}, you are not in the race!".format(ctx.message.author.display_name), delete_after=15)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(WikipediaSpeedrun(bot))
