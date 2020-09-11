import os, discord, pymongo, time, Constants
from dotenv import load_dotenv
from youtube_dl import YoutubeDL
from discord.ext import commands
load_dotenv()

bot = commands.Bot(command_prefix='!')

@bot.command(help="Trello link")
async def trello(ctx):
    await ctx.message.channel.send(Constants.TRELLO_LINK, delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
    await ctx.message.delete()

@bot.command(help="Rapport link")
async def rapport(ctx):
    await ctx.message.channel.send(Constants.RAPPORT_LINK, delete_after=Constants.DEFAULT_DELETE_WAIT_TIME)
    await ctx.message.delete()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(hidden=True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.message.delete()

@bot.command(hidden=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.message.delete()

for filename in os.listdir('./DiscordKarmaBot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
    
bot.run(os.getenv("TOKEN"))