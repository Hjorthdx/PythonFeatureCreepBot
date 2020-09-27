import discord, datetime
from discord.ext import commands

class Remindme(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.reminders = []
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Remindme cog is loaded")

    @commands.command(help="Test")
    async def remindme(self, ctx, time, text):
        if text is None:
            await ctx.send("No reminder text specified", delete_after=15)
        newReminder = reminder(time, text)
        self.reminders.append(newReminder)
        await ctx.send("I will remind you about {} in {}.".format(newReminder.text, newReminder.time))
        await newReminder.startReminder()
        await ctx.send("{}, you asked me to remind you about {}, {} ago.".format(ctx.author.name, text, time))

    @commands.command()
    async def currentReminders(self, ctx):
        await ctx.send("Throw new not implemented yet :P", delete_after=15)

    @commands.command()
    async def unremindme(self, ctx):
        await ctx.send("Throw new not implemented yet :D", delete_after=15)
        

def setup(bot):
    bot.add_cog(Remindme(bot))

import asyncio

class reminder():
    def __init__(self, time, text):
        self.time = time
        self.text = text
        self.totalSeconds = self.calculateTotalSeconds()

    def calculateTotalSeconds(self):
        days = 0
        hours = 0
        minutes = 0
        seconds = 0
        totalSeconds = 0
        remain = self.time
        if "days" in self.time.lower() or "day" in self.time.lower():
            days = self.time.split("day", 1)[0]
            remain = self.time.split("day", 1)[1]
            totalSeconds += int(days) * 60 * 60 * 24
        if "hours" in self.time.lower() or "hour" in self.time.lower():
            x = remain.split("hour",1)[0]
            remain = remain.split("hour", 1)[1]
            hours = [int(s) for s in x.split() if s.isdigit()]
            totalSeconds += hours[0] * 60 * 60
        if "minutes" in self.time.lower() or "minute" in self.time.lower():
            x = remain.split("minute",1)[0]
            remain = remain.split("minute", 1)[1]
            minutes = [int(s) for s in x.split() if s.isdigit()]
            totalSeconds += minutes[0] * 60
        if "seconds" in self.time.lower() or "second" in self.time.lower():
            x = remain.split("second",1)[0]
            remain = remain.split("second", 1)[1]
            seconds = [int(s) for s in x.split() if s.isdigit()]
            totalSeconds += seconds[0]

        if days:
            print(f"days: {days}")

        if hours:
            print(f"hours: {hours[0]}")
        
        if minutes:
            print(f"minutes: {minutes[0]}")

        if seconds:
            print(f"seconds: {seconds[0]}")

        print(totalSeconds)
        return totalSeconds

    async def startReminder(self):
        await asyncio.sleep(self.totalSeconds)
