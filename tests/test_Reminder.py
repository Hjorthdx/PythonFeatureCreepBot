'''
import unittest
import sys
sys.path.insert(0, "C:/Users/Sren/PycharmProjects/DiscordFeatureCreepBot/Cogs")
import Remindme #pylint: disable=import-error

class TestReminder(unittest.TestCase):
    def test_calculateTotalSeconds_DayHourMinuteSecond(self):
        dummyReminder = Remindme.reminder("1 day 1 hour 1 minute 1 second", "dummyText")
        expected = 90061  # 1 day 1 hour 1 minute 1 second
        self.assertEqual(expected, dummyReminder.totalSeconds)
    
    # Needs tests for:
    #   negative numbers
    #   Not all paramaters

'''