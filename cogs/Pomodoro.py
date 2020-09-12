import discord
from discord.ext import commands
import sys
sys.path.insert(0,"C:/Users/Sren/Documents/GitHub/DiscordKarmaBot")
import Db

class Pomodoro(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.defaultWorkTimer = 50
        self.defaultBreakTimer = 10
        self.currentTimers = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pomodoro cog is loaded")

    @commands.command(brief="Default value 50/10", help="!pomodoro x y, where x is work length and y is break length. Currently needs a name aswell, cause not fully operational yet. Working on it :D")
    async def pomodoro(self, ctx):
        # The sound that needs to be played
        pending_command = self.bot.get_command("PlayPomodoro")

        # Get lengths of pomdoro timer
        workLength, breakLength = self.getLengthsFromMessage(ctx.message)

        x = ctx.message.content.replace("!pomodoro", "")
        # Create new Timer object
        newTimer = Timer(x, workLength, breakLength, pending_command)

        # Formats the time data
        # Perhabs make this a function, so I don't have to look at it as Kurt would say.
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

        # Informs the user that a pomodoro has begun
        await ctx.send("Timer name: {} \nStarting timers: {} / {} minutes. \nWork ends at {} \nBreak ends at {}".format(newTimer.name, workLength / 60, breakLength / 60, workEndTime, breakEndTime), delete_after=newTimer.workLength + newTimer.breakLength)
        self.currentTimers.append(newTimer)
        await newTimer.startTimer(ctx)
        await ctx.message.delete()

    def getLengthsFromMessage(self, message):
        x = [int(s) for s in message.content.split() if s.isdigit()] # Gets all the digits from the string and saves in a list of integers.
        if len(x) == 0:
            return self.defaultWorkTimer * 60 , self.defaultBreakTimer * 60
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
        await ctx.send("remaining time on timer {}: {}".format(neededTimer.name,remainingTime), delete_after=15)
        await ctx.message.delete()

    @commands.command(help="!changeDefault work 50 e.g.")
    async def changeDefault(self, ctx):
        x = [int(s) for s in ctx.message.content.split() if s.isdigit()]
        if "work" in ctx.message.content:
            self.defaultWorkTimer = x[0]
        elif "break" in ctx.message.content:
            self.defaultBreakTimer = x[1]
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Pomodoro(bot))

import datetime, asyncio

class Timer():
    def __init__(self, name, workLength, breakLength, pending_command):
        self.name = name
        self.workLength = workLength
        self.breakLength = breakLength
        self.startingTime = datetime.datetime.now()
        self.workBool = True
        self.pending_command = pending_command

    async def startTimer(self, ctx):
        await self.workTimer(self.workLength)
        await ctx.send("Works over! Break starts now", delete_after=self.breakLength)
        await ctx.invoke(self.pending_command)
        
        await self.breakTimer(self.breakLength)
        await ctx.send("Breaks over!", delete_after=15)
        await ctx.invoke(self.pending_command)

    async def workTimer(self, workLength):
        self.workBool = True
        await asyncio.sleep(workLength)
        # Adds the work duration to the database.
        workPomodoro = {"Work duration:": workLength / 60,
                        "Work bool": self.workBool,
                        "Starting time": self.startingTime}
        Db.pomodoroCol.insert_one(workPomodoro)

    async def breakTimer(self, breakLength):
        self.workBool = False
        await asyncio.sleep(breakLength)
        # Adds the break duration to the database.
        breakPomodoro = {"Break duration:": breakLength / 60,
                        "Work bool": self.workBool,
                        "Starting time": self.startingTime}
        Db.pomodoroCol.insert_one(breakPomodoro)

    def calculateRemainingTime(self):
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