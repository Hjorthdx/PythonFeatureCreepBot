import discord
from discord.ext import commands

# When timer is expired, it still does not play a mp3 file.
# Tried hack right now, with the bot activating its own command through discord,
# But please think of better solution :D
class Pomodoro(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.currentTimers = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pomodoro cog is loaded")

    @commands.command(brief="Default value 50/10", help="!pomodoro x y, where x is work length and y is break length. Currently needs a name aswell, cause not fully operational yet. Working on it :D")
    async def pomodoro(self, ctx):
        # Get lengths of pomdoro timer
        workLength, breakLength = self.getLengthsFromMessage(ctx.message)

        x = ctx.message.content.replace("!test", "")
        # Create new Timer object
        newTimer = Timer(x, workLength, breakLength)

        # Tell users timer information
        # Should prob be in the timer object, if it can work with async.
        x = newTimer.startingTime + datetime.timedelta(seconds=workLength)
        if x.minute <= 9:
            workEndTime = "{}:{}:{}".format(x.hour, int(str(0) + str(x.minute)), x.second)
        else:
            workEndTime = "{}:{}:{}".format(x.hour, x.minute, x.second)
        
        y = newTimer.startingTime + datetime.timedelta(seconds=workLength + breakLength)
        if y.minute <= 9:
            breakEndTime = "{}:{}:{}".format(y.hour, int(str(0) + str(y.minute)), y.second)
        else:
            breakEndTime = "{}:{}:{}".format(y.hour, y.minute, y.second)

        await ctx.send("Timer: {} \nStarting timers: {} / {} minutes. \nWork ends at {} \nBreak ends at {}".format(newTimer.name, workLength / 60, breakLength / 60, workEndTime, breakEndTime), delete_after=newTimer.workLength + newTimer.breakLength)
        self.currentTimers.append(newTimer)
        await newTimer.startTimer(ctx)
        await ctx.message.delete()

    def getLengthsFromMessage(self, message):
        x = [int(s) for s in message.content.split() if s.isdigit()] # Gets all the digits from the string and saves in a list of integers.
        if len(x) == 0:
            return 60 , 60
        elif len(x) == 2:
            workLength = x[0]
            breakLength = x[1]
            return workLength * 60, breakLength * 60
        else:
            print("Something went wrong.")

    @commands.command(name='time', brief="Remaining time on pomodoro timer", help="!time timerName, currently needs this timer name cause its not fully operational yet :D")
    async def _time(self, ctx):
        x = ctx.message.content.replace("!time", "")
        neededTimer = self.currentTimers[0]
        for timer in self.currentTimers:
            if x == timer.name:
                neededTimer = timer
        remainingTime = neededTimer.calculateRemainingTime()
        await ctx.send("remaining time on timer {}: {}".format(neededTimer.name,remainingTime), delete_after=5)
        await ctx.message.delete()
        


def setup(bot):
    bot.add_cog(Pomodoro(bot))



import datetime, asyncio

class Timer():
    def __init__(self, name, workLength, breakLength):
        self.name = name
        self.workLength = workLength
        self.breakLength = breakLength
        self.startingTime = datetime.datetime.now()
        self.workBool = True

    async def startTimer(self, ctx):
        await self.workTimer(self.workLength)
        await ctx.send("!play lyt nu", delete_after=5)
        await ctx.send("Test work timer ended", delete_after=5)
        
        await self.breakTimer(self.breakLength)
        await ctx.send("!play lyt nu", delete_after=5)
        await ctx.send("Test break time ended", delete_after=5)

    async def workTimer(self, workLength):
        self.workBool = True
        await asyncio.sleep(workLength)

    async def breakTimer(self, breakLength):
        self.workBool = False
        await asyncio.sleep(breakLength)

    def calculateRemainingTime(self):
        print("Calculate called")
        hours = 0
        minutes = 0
        duration = datetime.datetime.now() - self.startingTime
        durationInSeconds = duration.total_seconds()

        if self.workBool:
            remainingTimeInSeconds = self.workLength - durationInSeconds
        else:
            remainingTimeInSeconds = self.breakLength - durationInSeconds
        
        if remainingTimeInSeconds > 3600:
            hours, remainingTimeInSeconds = divmod(remainingTimeInSeconds, 3600)
        if remainingTimeInSeconds > 60:
            minutes, remainingTimeInSeconds = divmod(remainingTimeInSeconds, 60)

        formattedRemainingTime=('%02d:%02d:%02d'%(hours,minutes,remainingTimeInSeconds))
        print(formattedRemainingTime)
        return formattedRemainingTime