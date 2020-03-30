import threading
import bot

def start(workLength, breakLength, channel):
    workTimer = threading.Timer(workLength, printer(channel))
    breakTimer = threading.Timer(workLength + breakLength, printer2)
    workTimer.start()
    breakTimer.start()


def printer(channel):
    print("a")

def printer2():
    print("Break done")

