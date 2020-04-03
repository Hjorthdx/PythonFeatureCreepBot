import discord, asyncio, Constants, Player, datetime


async def startTimers(message):
    workLength, breakLength = getLengths(message.content)
    #workLength = workLength * 60
    #breakLength = breakLength * 60
    print(workLength)
    print(breakLength)
    await workTimer(message, workLength, breakLength)

async def workTimer(message, workLength, breakLength):
    await asyncio.sleep(workLength)
    await message.channel.send("WORKS OVER, STARTING BREAK")
    await Player.playTimerEnd(message.author.voice.channel)
    await breakTimer(message, breakLength)

async def breakTimer(message, breakLength):
    await asyncio.sleep(breakLength)
    await message.channel.send("BREAKS OVER")
    await Player.playTimerEnd(message.author.voice.channel)

def getLengths(content):
    x = [int(s) for s in content.split() if s.isdigit()] # Gets all the digits from the string and saves in a list of integers.
    if len(x) == 0:
        return Constants.DEFAULT_WORKTIME * 60, Constants.DEFAULT_BREAKTIME * 60
    elif len(x) == 2:
        workLength = x[0]
        breakLength = x[1]
        return workLength * 60, breakLength * 60
    else:
        print('Wrong formatted user input')
        # Should text this to the user

def calculateRemainingTime():
    return 1
