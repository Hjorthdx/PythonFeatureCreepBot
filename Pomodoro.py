import discord, asyncio, Constants, Player, datetime, Db

startingTime = 0
workBool = False

# Ændre message.content her til bamse her, så default case ikke også er bamse hvis man skriver forkert
# Måske skal start timers bare klare det hele i en funktion. Tror det er derfor break spiller to gange. Giv det evt et forsøg.

async def startTimers(message):
    global workLength
    global breakLength
    workLength, breakLength = getLengths(message)
    global startingTime
    startingTime = datetime.datetime.now()
    await message.channel.send("Starting timers: {} / {} minutes.".format(workLength / 60, breakLength / 60))
    await workTimer(message, workLength, breakLength)

async def workTimer(message, workLength, breakLength):
    global workBool 
    workBool = True
    await asyncio.sleep(workLength)
    workPomodoro = {"Work duration:": workLength / 60,
                    "Work bool": workBool,
                    "Starting time": startingTime}
    Db.pomodoroCol.insert_one(workPomodoro)
    await message.channel.send("WORKS OVER!! Hold pause forhelvede")
    await Player.play(True)
    print("Test 1")
    await breakTimer(message, breakLength)

async def breakTimer(message, breakLength):
    global workBool
    workBool = False
    await asyncio.sleep(breakLength)
    breakPomodoro = {"Break duration:": breakLength / 60,
                    "Work bool": workBool,
                    "Starting time": startingTime}
    Db.pomodoroCol.insert_one(breakPomodoro)
    await message.channel.send("BREAKS OVER")
    print("Test 2")
    await Player.play(True)

# Really only needs message.content, but I need to know the channel to send error msg.
# Maybe this is fixable with just some time to think about it.
def getLengths(message):
    x = [int(s) for s in message.content.split() if s.isdigit()] # Gets all the digits from the string and saves in a list of integers.
    if len(x) == 0:
        return Constants.DEFAULT_WORKTIME * 60, Constants.DEFAULT_BREAKTIME * 60
    elif len(x) == 2:
        workLength = x[0]
        breakLength = x[1]
        return workLength * 60, breakLength * 60
    else:
        print("Something went wrong.")

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