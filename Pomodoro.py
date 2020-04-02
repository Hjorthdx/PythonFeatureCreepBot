import threading, Constants, discord, asyncio

def startTimer(message): # IS IN SECONDS RN
    workLength, breakLength = getLengths(message.content) # AD
    workTimer = threading.Timer(workLength, printer, [message])
    breakTimer = threading.Timer(workLength + breakLength, printer2, [message])
    workTimer.start()
    breakTimer.start()

def getLengths(content):
    x = [int(s) for s in content.split() if s.isdigit()] # This gets all the digits from the string and saves in a list of integers.
    if len(x) == 0:
        return Constants.DEFAULT_WORKTIME, Constants.DEFAULT_BREAKTIME
    elif len(x) == 2:
        workLength = x[0]
        breakLength = x[1]
        return workLength, breakLength
    else:
        print('Wrong formatted user input')
        # Should text this to the user

def printer(message):
    print("Work done")
    # Kind of annoying to send message I need to await message.channel.send,
    # but I can't await cause function is not async, and I can't make it,
    # cause I can't await inside the threading.Timer.
    # There has to be a solve for this. Just can't see it right now, it's late.
    # Goodluck future Hjorth_

def printer2(message):
    print("Break done")

