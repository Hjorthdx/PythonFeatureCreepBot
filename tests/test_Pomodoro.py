import unittest
import datetime
from unittest import mock
from cogs import Pomodoro


class TestPomodoro(unittest.TestCase):

    def test_PomodoroManager_start_new_pomodoro_name_is_none(self):
        expected = Pomodoro.PomodoroTimer(category_id=1, work_duration=50, break_duration=10, name=None)
        pomodoro_manager = Pomodoro.PomodoroManager()
        result = pomodoro_manager.start_new_pomodoro(category_id=1, work_duration=50, break_duration=10, name=None)
        self.assertEqual(result, expected)

    def test_PomodoroManager_start_new_pomodoro_name_is_not_none(self):
        expected = Pomodoro.PomodoroTimer(category_id=1, work_duration=50, break_duration=10, name="Test")
        pomodoro_manager = Pomodoro.PomodoroManager()
        result = pomodoro_manager.start_new_pomodoro(category_id=1, work_duration=50, break_duration=10, name="Test")
        self.assertEqual(result, expected)

    def test_PomodoroManager_find_pomodoro_timer_name_is_none(self):
        expected = Pomodoro.PomodoroTimer(category_id=1, work_duration=50, break_duration=10, name=None)
        pomodoro_manager = Pomodoro.PomodoroManager()
        new_pomodoro_timer = pomodoro_manager.start_new_pomodoro(category_id=1, work_duration=50, break_duration=10,
                                                                 name=None)
        result = pomodoro_manager.find_pomodoro_timer(category_id=new_pomodoro_timer.category_id)
        self.assertEqual(result[0], expected)

    def test_PomodoroManager_find_pomodoro_timer_name_is_not_none(self):
        expected = Pomodoro.PomodoroTimer(category_id=1, work_duration=50, break_duration=10, name="Test")
        pomodoro_manager = Pomodoro.PomodoroManager()
        new_pomodoro_timer = pomodoro_manager.start_new_pomodoro(category_id=1, work_duration=50, break_duration=10,
                                                                 name="Test")
        result = pomodoro_manager.find_pomodoro_timer(name=new_pomodoro_timer.name)
        self.assertEqual(result[0], expected)

    def test_PomodoroManager_find_pomodoro_timer_name_and_category_not_none(self):
        expected = Pomodoro.PomodoroTimer(category_id=1, work_duration=50, break_duration=10, name="Test")
        pomodoro_manager = Pomodoro.PomodoroManager()
        new_pomodoro_timer = pomodoro_manager.start_new_pomodoro(category_id=1, work_duration=50, break_duration=10,
                                                                 name="Test")
        result = pomodoro_manager.find_pomodoro_timer(category_id=new_pomodoro_timer.category_id,
                                                      name=new_pomodoro_timer.name)
        self.assertEqual(result[0], expected)

    def test_PomodoroManager_find_pomodoro_timer_name_and_category_is_none(self):
        expected = []
        pomodoro_manager = Pomodoro.PomodoroManager()
        new_pomodoro_timer = pomodoro_manager.start_new_pomodoro(category_id=1, work_duration=50, break_duration=10,
                                                                 name="Test")
        result = pomodoro_manager.find_pomodoro_timer(category_id=None, name=None)
        self.assertEqual(result, expected)

    def test_PomodoroManager_find_pomodoro_timer_name_is_not_correct_and_no_category(self):
        expected = []
        pomodoro_manager = Pomodoro.PomodoroManager()
        new_pomodoro_timer = pomodoro_manager.start_new_pomodoro(category_id=1, work_duration=50, break_duration=10,
                                                                 name="Test")
        result = pomodoro_manager.find_pomodoro_timer(category_id=None, name="test")
        self.assertEqual(result, expected)

    def test_PomodoroManager_find_pomodoro_timer_name_is_not_correct_and_category_not_none(self):
        expected = Pomodoro.PomodoroTimer(category_id=1, work_duration=50, break_duration=10, name="Test")
        pomodoro_manager = Pomodoro.PomodoroManager()
        new_pomodoro_timer = pomodoro_manager.start_new_pomodoro(category_id=1, work_duration=50, break_duration=10,
                                                                 name="Test")
        result = pomodoro_manager.find_pomodoro_timer(category_id=new_pomodoro_timer.category_id, name="test")
        self.assertEqual(result[0], expected)

    def test_PomodoroTimer_get_end_work_time(self):
        work_duration = datetime.timedelta(minutes=50)
        break_duration = datetime.timedelta(minutes=10)
        pomodoro_timer = Pomodoro.PomodoroTimer(category_id=1, work_duration=work_duration,
                                                break_duration=break_duration, name="Test")
        expected = datetime.datetime.now() + work_duration
        result = pomodoro_timer.get_end_work_time()
        self.assertEqual(result, expected)

    def test_PomodoroTimer_get_break_work_time(self):
        work_duration = datetime.timedelta(minutes=50)
        break_duration = datetime.timedelta(minutes=10)
        pomodoro_timer = Pomodoro.PomodoroTimer(category_id=1, work_duration=work_duration,
                                                break_duration=break_duration, name="Test")
        expected = datetime.datetime.now() + work_duration + break_duration
        result = pomodoro_timer.get_end_break_time()
        self.assertEqual(result, expected)

    def test_PomodoroTimer_is_work_over_work_timer_in_the_past(self):
        work_duration = datetime.timedelta(minutes=50)
        break_duration = datetime.timedelta(minutes=10)
        timer = Pomodoro.Timer(work_duration)
        timer.starting_time = datetime.datetime(2020, 12, 24)
        pomodoro_timer = Pomodoro.PomodoroTimer(category_id=1, work_duration=work_duration,
                                                break_duration=break_duration, name="Test")
        pomodoro_timer.work_timer = timer
        expected = True
        result = pomodoro_timer.is_work_over()
        self.assertEqual(result, expected)

    def test_PomodoroTimer_is_work_over_work_timer_in_the_future(self):
        work_duration = datetime.timedelta(minutes=50)
        break_duration = datetime.timedelta(minutes=10)
        timer = Pomodoro.Timer(work_duration)
        timer.starting_time = datetime.datetime(2100, 12, 24)
        pomodoro_timer = Pomodoro.PomodoroTimer(category_id=1, work_duration=work_duration,
                                                break_duration=break_duration, name="Test")
        pomodoro_timer.work_timer = timer
        expected = False
        result = pomodoro_timer.is_work_over()
        self.assertEqual(result, expected)

    # Not sure if this is a good test actually.
    def test_Timer_get_remaining_time(self):
        timer = Pomodoro.Timer(datetime.timedelta(minutes=50))
        timer.starting_time = datetime.datetime.now()
        result = timer.get_remaining_time()
        expected = datetime.timedelta(minutes=50) - (datetime.datetime.now() - timer.starting_time)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
