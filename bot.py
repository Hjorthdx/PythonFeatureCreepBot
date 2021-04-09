import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)


@bot.command(hidden=True)
async def load(ctx, extension):
    if ctx.author.id == 140195461519769601:
        bot.load_extension(f'cogs.{extension}')


@bot.command(hidden=True)
async def unload(ctx, extension):
    if ctx.author.id == 140195461519769601:
        bot.unload_extension(f'cogs.{extension}')


@bot.command(hidden=True)
async def reload(ctx, extension):
    if ctx.author.id == 140195461519769601:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    #await get_everything_from_migmig_channel()
    #await get_all_memes_from_migmig_channel_that_has_remouladeklat_or_opdut()
    #total, opduts, nedduts = await recount_karma()
    #print(total)
    #print(opduts)
    #print(nedduts)


@bot.event
async def on_command_completion(ctx):
    await ctx.message.delete()


@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send(error, delete_after=15)
    await ctx.message.delete()


# Has two functionalities right now. This should be fixed and moved into two different methods xd
async def recount_karma():
    channel = bot.get_channel(619105859615719434)
    messages = await channel.history(limit=2000).flatten()
    print(len(messages))
    total, opduts, nedduts = 0, 0, 0
    author_id = 103033943464353792 # Insert here future me :)
    for message in messages:
        if message.author.id == author_id:
            if message.reactions is not None:
                for reaction in message.reactions:
                    try:
                        if reaction.emoji.id == 619818932475527210:
                            opduts += reaction.count
                        elif reaction.emoji.id == 651028634945060864:
                            nedduts += reaction.count
                    except AttributeError as e:
                        print(e)

    total = opduts - nedduts
    return total, opduts, nedduts


async def get_all_memes_from_migmig_channel_that_has_remouladeklat_or_opdut():
    channel = bot.get_channel(619105859615719434)
    messages = await channel.history(limit=None).flatten()
    print(len(messages))
    for message in messages:
        if message.reactions is not None:
            if message.attachments is not None:
                for reaction in message.reactions:
                    try:
                        if reaction.emoji.id == 619818932475527210 or reaction.emoji.id == 619197419137007644:
                            for attachment in message.attachments:
                                print(f'id: {message.author.display_name}, filename: {attachment.filename}')
                                await attachment.save(str(reaction.count) + str(message.author.display_name) + str(attachment.id) + attachment.filename)
                    except AttributeError as e:
                        print(f'{e}, message author: {message.author.display_name}')


async def get_everything_from_migmig_channel():
    channel = bot.get_channel(619105859615719434)
    messages = await channel.history(limit=None).flatten()
    print(len(messages))
    for message in messages:
        if message.attachments is not None:
            for attachment in message.attachments:
                if attachment.filename.endswith('.png') or attachment.filename.endswith('.jpg') or attachment.filename.endswith('.mp3') or attachment.filename.endswith('.mp4'):
                    print(f'id: {message.author.display_name}, filename: {attachment.filename}')
                    await attachment.save(str(message.author.display_name) + str(attachment.id) + attachment.filename)


for filename in os.listdir('C:/Users/Sren/PycharmProjects/DiscordFeatureCreepBot/cogs/'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.getenv("TOKEN"))
