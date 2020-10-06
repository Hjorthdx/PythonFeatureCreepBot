import discord
from discord.ext import commands


class Project(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.current_pins = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Project cog is loaded")

    @commands.command(help="Trello link")
    async def trello(self, ctx):
        await ctx.message.channel.send("https://trello.com/b/iFsYL4QH/weight-completion", delete_after=15)
        await ctx.message.delete()

    @commands.command(help="Rapport link")
    async def rapport(self, ctx):
        await ctx.message.channel.send("https://www.overleaf.com/project/5f56101b9841ac000168e006", delete_after=15)
        await ctx.message.delete()

    @commands.command(help="Pin something")
    async def pin(self, ctx, *, text):
        self.current_pins.append(text)
        await ctx.send(f"{text}, is now pinned", delete_after=15)
        await ctx.message.delete()

    @commands.command(name="pins", help="Current pins")
    async def current_pins(self, ctx):
        if not self.current_pins:
            await ctx.send("No current pins! .pin to pin something", delete_after=15)
        all_reminders = ""
        count = 0
        for pin in self.current_pins:
            all_reminders += str(count)
            all_reminders += " - "
            all_reminders += pin
            all_reminders += "\n"
            count += 1

        await ctx.send(all_reminders, delete_after=15)
        await ctx.message.delete()

    @commands.command(name="unpin", help="Removes pin from index")
    async def remove_pins(self, ctx, *, index: int):
        if index < 0:
            print("Index cant be less than zero")
        #elif index > len(self.current_pins): IDK ITS STUPID RN AND I CBA
        #    print("Index higher than length of current pins")
        else:
            self.current_pins.pop(index)
            await ctx.send(f"Removed pin at {index}", delete_after=15)

        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Project(bot))
