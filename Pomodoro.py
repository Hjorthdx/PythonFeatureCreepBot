import threading

def startTimer(workLength, breakLength, channel): # IS IN SECONDS RN
    workTimer = threading.Timer(workLength, printer(channel))
    breakTimer = threading.Timer(workLength + breakLength, printer2)
    workTimer.start()
    breakTimer.start()

def printer(channel):
    print("a")

def printer2():
    print("Break done")

