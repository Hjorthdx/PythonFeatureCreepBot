import discord, datetime, wikipedia
from discord.ext import commands


# import sys
# sys.path.insert(0,"C:/Users/Sren/Documents/GitHub/DiscordKarmaBot")
# import Db #pylint: disable=import-error

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
        x = self.currentRun.add_competitor(ctx.message.author.display_name)
        if x == 0:  # If player is already in the race
            await ctx.send("{}, you are already in the race! Stand by!".format(ctx.message.author.display_name),
                           delete_after=15)
        else:
            if self.currentPlayerMsg is None:  # If it is the first message send
                await ctx.send("{} joined the race! \n".format(ctx.message.author.display_name), delete_after=15)
                self.currentPlayerMsg = await ctx.send("Current players are: \n{}".format(self.currentRun.participants))
            else:
                await ctx.send("{} joined the race! \n".format(ctx.message.author.display_name), delete_after=15)
                await self.currentPlayerMsg.edit(
                    content="Current players are: \n{}".format(self.currentRun.participants))
        await ctx.message.delete()

    @commands.command(help="Leave the race")
    async def leave(self, ctx):
        x = self.currentRun.remove_competitor(ctx.message.author.display_name)
        if x == 0:  # If player is not the in the race
            await ctx.send("{}, you are not in the race!".format(ctx.message.author.display_name), delete_after=15)
        else:
            if len(self.currentRun.participants) == 0:  # If there is no players left in the race
                await self.currentPlayerMsg.delete()
                self.currentPlayerMsg = None
                await ctx.send("{} left the race.".format(ctx.message.author.display_name), delete_after=15)
            else:
                await ctx.send("{} left the race.".format(ctx.message.author.display_name), delete_after=15)
                await self.currentPlayerMsg.edit(
                    content="Current players are: \n{}".format(self.currentRun.participants))
        await ctx.message.delete()

    @commands.command(brief="Goal article link")
    async def goal(self, ctx):
        x = self.currentRun.set_goal_article(ctx.message.author.display_name, ctx.message.content.replace("!goal", ""))
        if x == 0:  # If the player is in the face and the goal is not yet defined
            self.goalArticleMsg = await ctx.send("The article to find is: {}".format(self.currentRun.endArticle))
            await self.goalArticleMsg.edit(suppress=True)
        elif x == 1:  # If the goal is already defined
            await ctx.send("End article is already set!", delete_after=15)
        elif x == 2:  # If the player is not in the race
            await ctx.send(
                "{}, you are not in the race. Join the race to set the goal".format(ctx.message.author.display_name),
                delete_after=15)
        await ctx.message.delete()

    @commands.command(brief="Starts the run", help="Atleast two competitors are needed to start a race.")
    async def start(self, ctx):
        x = self.currentRun.start_race()
        if x == 0:  # If there isn't enough players
            await ctx.send("Not enough competitors <:Spand:619148485379358739>", delete_after=15)
        elif x == 1:  # If the goal is not defined
            await ctx.send("The goal is not set. Use !goal to set the goal.", delete_after=15)
        else:
            await ctx.send("The race has begun!", delete_after=15)
            self.startingArticleMsg = await ctx.send(self.currentRun.startingArticle)
        await ctx.message.delete()

    @commands.command(help="Ends the run and announces winner + elapsed time")
    async def done(self, ctx):
        x = self.currentRun.end_race(ctx.message.author.display_name)
        if x == 0:
            await ctx.send("{} is the winner! Finding the article in: {}".format(ctx.message.author.display_name,
                                                                                 self.currentRun.finalTime),
                           delete_after=30)
            self.currentRun = Speedrun()
            await self.currentPlayerMsg.delete()
            await self.startingArticleMsg.delete()
            await self.goalArticleMsg.delete()
        else:
            await ctx.send("{}, you are not in the race!".format(ctx.message.author.display_name), delete_after=15)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(WikipediaSpeedrun(bot))


class Speedrun:
    def __init__(self):
        self.participants = []
        self.startingTime = None
        self.finalTime = None
        self.startingArticle = self.get_starting_article()
        self.endArticle = None
        self.winner = None

    @staticmethod
    def get_starting_article():
        while True:
            try:
                return wikipedia.page(wikipedia.random(1)).url
            except wikipedia.DisambiguationError:
                print("DisambiguationError")
                continue

    def add_competitor(self, name):
        if name in self.participants:
            return 0
        else:
            self.participants.append(name)
            return 1

    def remove_competitor(self, name):
        if name not in self.participants:
            return 0
        else:
            self.participants.remove(name)
            return 1

    def set_goal_article(self, name, endArticle):
        if name in self.participants and self.endArticle is None:
            self.endArticle = endArticle
            return 0
        elif self.endArticle is not None:
            return 1
        elif name not in self.participants:
            return 2

    def start_race(self):
        if len(self.participants) < 2:
            return 0
        elif self.endArticle is None:
            return 1
        else:
            self.startingTime = datetime.datetime.now()
            return 2

    def end_race(self, name):
        if name in self.participants:
            self.format_time()
            self.winner = name
            self.save_run_to_database()
            return 0

    def format_time(self):
        x = datetime.datetime.now() - self.startingTime
        seconds_left = x.total_seconds()
        hours = 0
        minutes = 0
        if seconds_left > 3600:
            hours, seconds_left = divmod(seconds_left, 3600)
        if seconds_left > 60:
            minutes, seconds_left = divmod(seconds_left, 60)
        self.finalTime = ('%02d:%02d:%02d' % (hours, minutes, seconds_left))

    def save_run_to_database(self):
        run = {"Participants": self.participants,
               "Starting article": self.startingArticle,
               "Goal article": self.endArticle,
               "Winner": self.winner}
        # Db.wikipediaSpeedrunCol.insert_one(run)
