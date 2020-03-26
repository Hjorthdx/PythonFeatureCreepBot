import time
import datetime as dt

def startPomodoro(pomodoro_time, break_time):
    print("Pomodoro started")
    start_time = dt.datetime.now()
    pomodoro_time = pomodoro_time
    time_delta = dt.timedelta(0,pomodoro_time)
    pomodoro_end_time = start_time + time_delta
    break_time = break_time

    if start_time < pomodoro_end_time:
        print("Currently working")


