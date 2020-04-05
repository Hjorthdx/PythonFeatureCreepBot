import discord, asyncio, Constants, Player, datetime

startingTime = 0
workBool = False

async def startTimers(message):
    global workLength
    global breakLength
    workLength, breakLength = getLengths(message.content)
    global startingTime
    startingTime = datetime.datetime.now()
    await workTimer(message, workLength, breakLength)

async def workTimer(message, workLength, breakLength):
    global workBool 
    workBool = True
    await asyncio.sleep(workLength)
    await message.channel.send("WORKS OVER, STARTING BREAK")
    await Player.playTimerEnd(message.author.voice.channel)
    await breakTimer(message, breakLength)

async def breakTimer(message, breakLength):
    global workBool
    workBool = False
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
        # Should maybe text this to the user

def calculateRemainingTime():
    global startingTime
    global workLength
    global workLength
    global workBool
    hours = 0
    duration = datetime.datetime.now() - startingTime
    durationInSeconds = duration.total_seconds()

    if workBool:
        remainingTimeInSeconds = workLength - durationInSeconds
    else:
        remainingTimeInSeconds = breakLength - durationInSeconds
    
    if remainingTimeInSeconds > Constants.SECONDS_IN_HOUR:
        hours, remainingTimeInSeconds = divmod(remainingTimeInSeconds, 3600)
    if remainingTimeInSeconds > Constants.SECONDS_IN_MINUTE:
        minutes, remainingTimeInSeconds = divmod(remainingTimeInSeconds, 60)

    formattedRemainingTime=('%02d:%02d:%02d'%(hours,minutes,remainingTimeInSeconds))
    return formattedRemainingTime