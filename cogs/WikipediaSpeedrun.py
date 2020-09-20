import discord, datetime, wikipedia
from discord.ext import commands
import sys
sys.path.insert(0,"C:/Users/Sren/Documents/GitHub/DiscordKarmaBot")
import Db #pylint: disable=import-error

class WikipediaSpeedrun(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.currentRun = Speedrun()
        self.currentPlayerMsg = None
        self.startingArticleMsg = None
        self.goalArticleMsg = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("WikipediaSpeedrun cog is loaded")

    @commands.command(help="Join the race")
    async def join(self, ctx):
        x = self.currentRun.addCompetitor(ctx.message.author.display_name)
        if x == 0: # If player is already in the race
            await ctx.send("{}, you are already in the race! Stand by!".format(ctx.message.author.display_name), delete_after=15)
        else:
            if self.currentPlayerMsg is None: # If it is the first message send
                await ctx.send("{} joined the race! \n".format(ctx.message.author.display_name), delete_after=15)
                self.currentPlayerMsg = await ctx.send("Current players are: \n{}".format(self.currentRun.participants))
            else:
                await ctx.send("{} joined the race! \n".format(ctx.message.author.display_name), delete_after=15)
                await self.currentPlayerMsg.edit(content="Current players are: \n{}".format(self.currentRun.participants))
        await ctx.message.delete()
        
    @commands.command(help="Leave the race")
    async def leave(self, ctx):
        x = self.currentRun.removeCompetitor(ctx.message.author.display_name)
        if x == 0: # If player is not the in the race
            ctx.send("{}, you are not in the race!".format(ctx.message.author.display_name), delete_after=15)
        else:
            if len(self.currentRun.participants) == 0: # If there is no players left in the race
                await self.currentPlayerMsg.delete()
                self.currentPlayerMsg = None
                await ctx.send("{} left the race.".format(ctx.message.author.display_name), delete_after=15)
            else:
                await ctx.send("{} left the race.".format(ctx.message.author.display_name), delete_after=15)
                await self.currentPlayerMsg.edit(content="Current players are: \n{}".format(self.currentRun.participants))
        await ctx.message.delete()

    @commands.command(brief="!goal article link")
    async def goal(self, ctx):
        x = self.currentRun.setGoalArticle(ctx.message.author.display_name, ctx.message.content.replace("!goal", ""))
        if x == 0: # If the player is in the face and the goal is not yet defined
            self.goalArticleMsg = await ctx.send("The article to find is: {}".format(self.currentRun.endArticle))
            await self.goalArticleMsg.edit(suppress=True)
        elif x == 1: # If the goal is already defined
            await ctx.send("End article is already set!", delete_after=15)
        elif x == 2: # If the player is not in the race
            await ctx.send("{}, you are not in the race. Join the race to set the goal".format(ctx.message.author.display_name), delete_after=15)
        await ctx.message.delete()
        
    @commands.command(brief="Starts the run", help="Atleast two competitors are needed to start a race.")
    async def start(self, ctx):
        x = self.currentRun.startRace()
        if x == 0: # If there isnt enough players
            await ctx.send("Not enough competitors <:Spand:619148485379358739>", delete_after=15)
        elif x == 1: # If the goal is not defined
            await ctx.send("The goal is not set. Use !goal to set the goal.", delete_after=15)
        else:
            await ctx.send("The race has begun!", delete_after=15)
            self.startingArticleMsg = await ctx.send(self.currentRun.startingArticle)
        await ctx.message.delete()

    @commands.command(help="Ends the run and announces winner + elapsed time")
    async def done(self, ctx):
        x = self.currentRun.endRace(ctx.message.author.display_name)
        if x == 0:
            await ctx.send("{} is the winner! Finding the article in: {}".format(ctx.message.author.display_name, self.currentRun.finalTime), delete_after=30)
            self.currentRun = Speedrun()
            await self.currentPlayerMsg.delete()
            await self.startingArticleMsg.delete()
            await self.goalArticleMsg.delete()
        else:
            await ctx.send("{}, you are not in the race!".format(ctx.message.author.display_name), delete_after=15)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(WikipediaSpeedrun(bot))

class Speedrun():
    def __init__(self):
        self.participants = []
        self.startingTime = None
        self.finalTime = None
        self.startingArticle = self.getStartingArticle()
        self.endArticle = None
        self.winner = None
    
    def getStartingArticle(self):
        while True:
            try:
                return wikipedia.page(wikipedia.random(1)).url
            except: # DisambiguationError
                print("DisambiguationError")
                continue
            else:
                break

    def addCompetitor(self, name):
        if name in self.participants:
            return 0
        else:
            self.participants.append(name)
            return 1

    def removeCompetitor(self, name):
        if name not in self.participants:
            return 0
        else:
            self.participants.remove(name)
            return 1

    def setGoalArticle(self, name, endArticle):
        if name in self.participants and self.endArticle == None:
            self.endArticle = endArticle
            return 0
        elif self.endArticle != None:
            return 1
        elif name not in self.participants:
            return 2   

    def startRace(self):
        if len(self.participants) < 2:
            return 0
        elif self.endArticle == None:
            return 1
        else:
            self.startingTime = datetime.datetime.now()
            return 2

    def endRace(self, name):
        if name in self.participants:
            self.formatTime()
            self.winner = name
            self.saveRunToDatabase()
            return 0

    def formatTime(self):
        x = datetime.datetime.now() - self.startingTime
        secondsLeft = x.total_seconds()
        hours = 0
        minutes = 0
        if secondsLeft > 3600:
            hours, secondsLeft = divmod(secondsLeft, 3600)
        if secondsLeft > 60:
            minutes, secondsLeft = divmod(secondsLeft, 60)
        self.finalTime=('%02d:%02d:%02d'%(hours,minutes,secondsLeft))

    def saveRunToDatabase(self):
        run = {"Participants": self.participants,
               "Starting article": self.startingArticle,
               "Goal article": self.endArticle,
               "Winner": self.winner}
        Db.wikipediaSpeedrunCol.insert_one(run)
