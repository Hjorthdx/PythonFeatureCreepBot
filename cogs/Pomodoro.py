import discord
from discord.ext import commands
#import sys
#sys.path.insert(0,"C:/Users/Sren/Documents/GitHub/DiscordKarmaBot")
#import Db #pylint: disable=import-error

class Pomodoro(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.defaultWorkTimer = 50
        self.defaultBreakTimer = 10
        self.currentTimers = []
        self.testCounter = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pomodoro cog is loaded")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None:
            self.testCounter = self.testCounter - 1
        elif before is None and after is not None:
            self.testCounter = self.testCounter + 1
        
        if self.testCounter >= 2 and not self.currentTimers:
            x = self.bot.get_channel(619094316106907660)
            await x.send("Pomodoro?", delete_after=300)

    @commands.command(brief="Default value 50/10", help=".pomodoro x y, where x is work length and y is break length.", aliases=['p'])
    async def pomodoro(self, ctx):
        playcmd = self.bot.get_command("PlayPomodoro")
        workLength, breakLength = self.getLengthsFromMessage(ctx.message)
        x = ctx.message.content.replace(".pomodoro", "")
        newTimer = Timer(x, workLength, breakLength)
        workEndTime, breakEndTime = self.formatTime(workLength, breakLength, newTimer)
        await ctx.send("Timer name: {} \nStarting timers: {} / {} minutes. \nWork ends at {} \nBreak ends at {}".format(newTimer.name, workLength / 60, breakLength / 60, workEndTime, breakEndTime), delete_after=newTimer.workLength + newTimer.breakLength)
        self.currentTimers.append(newTimer)

        await newTimer.workTimer()
        await ctx.send("Works over! Break starts now", delete_after=breakLength)
        # Ensures voice. This is a "hack".
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
        await ctx.invoke(playcmd)

        await newTimer.breakTimer()
        await ctx.send("Breaks over!", delete_after=15)

        # Ensures voice. This is a "hack".
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
        await ctx.invoke(playcmd)
        
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

    def formatTime(self, workLength, breakLength, newTimer):
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

        return workEndTime, breakEndTime

    @commands.command(name='time', brief="Remaining time on pomodoro timer", help="time timerName, currently needs this timer name cause its not fully operational yet :D")
    async def _time(self, ctx):
        x = ctx.message.content.replace(".time", "")
        neededTimer = self.currentTimers[0]
        for timer in self.currentTimers:
            if x == timer.name:
                neededTimer = timer
        remainingTime = neededTimer.calculateRemainingTime()
        await ctx.send("remaining time on timer {}: {}".format(neededTimer.name,remainingTime), delete_after=15)
        await ctx.message.delete()

    @commands.command(help=".changeDefault work 50 e.g.")
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
    def __init__(self, name, workLength, breakLength):
        self.name = name
        self.workLength = workLength
        self.breakLength = breakLength
        self.startingTime = datetime.datetime.now()
        self.workBool = True

    async def workTimer(self):
        self.workBool = True
        await asyncio.sleep(self.workLength)
        #workPomodoro = {"Work duration:": self.workLength / 60,
        #                "Work bool": self.workBool,
        #                "Starting time": self.startingTime}
        #Db.pomodoroCol.insert_one(workPomodoro)

    async def breakTimer(self):
        self.workBool = False
        await asyncio.sleep(self.breakLength)
        #breakPomodoro = {"Break duration:": self.breakLength / 60,
        #                "Work bool": self.workBool,
        #                "Starting time": self.startingTime}
        #Db.pomodoroCol.insert_one(breakPomodoro)

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