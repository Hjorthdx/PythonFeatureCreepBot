import unittest, datetime
import sys
sys.path.insert(0,"C:/Users/Sren/Documents/GitHub/DiscordKarmaBot/cogs")
import WikipediaSpeedrun

class TestSpeedrun(unittest.TestCase):
    def test_addCompetitor_emptyList(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        expected = ["Test"]
        dummySpeedrun.addCompetitor("Test")
        self.assertCountEqual(expected, dummySpeedrun.participants)

    def test_addCompetitor_NonEmptyList(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        expected = ["Test", "Test2"]
        dummySpeedrun.participants = ["Test2"]
        dummySpeedrun.addCompetitor("Test")
        self.assertCountEqual(expected, dummySpeedrun.participants)

    def test_addCompetitor_AlreadyInList(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        dummySpeedrun.participants = ["Test"]
        self.assertEqual(0, dummySpeedrun.addCompetitor("Test"))

    def test_removeCompetitor_emptyList(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        self.assertEqual(0, dummySpeedrun.removeCompetitor("Test"))

    def test_removeCompetitor_AlreadyInList(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        expected = ["Test2"]
        dummySpeedrun.participants = ["Test", "Test2"]
        dummySpeedrun.removeCompetitor("Test")
        self.assertCountEqual(expected, dummySpeedrun.participants)

    def test_removeCompetitor_AlreadyInListOneParticipantOnly(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        expected = []
        dummySpeedrun.participants = ["Test"]
        dummySpeedrun.removeCompetitor("Test")
        self.assertCountEqual(expected, dummySpeedrun.participants)

    def test_setGoalArticle_NonParticipantingUser(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        expected = None
        dummySpeedrun.setGoalArticle("Test", "dummyUrl")
        self.assertEqual(expected, dummySpeedrun.endArticle)

    def test_setGoalArticle_EndArticleAlreadySet(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        dummySpeedrun.endArticle = "dummyUrl"
        expected = "dummyUrl"
        dummySpeedrun.setGoalArticle("Test", "dummyUrl2")
        self.assertEqual(expected, dummySpeedrun.endArticle)

    def test_setGoalArticle_ParticipatingUserNoEndArticle(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        dummySpeedrun.participants = ["Test"]
        expected = "dummyUrl"
        dummySpeedrun.setGoalArticle("Test", "dummyUrl")
        self.assertEqual(expected, dummySpeedrun.endArticle)

    def test_startRace_NotEnoughParticipants(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        self.assertEqual(0, dummySpeedrun.startRace())

    def test_startRace_NoEndArticle(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        dummySpeedrun.participants = ["Test", "Test2"]
        self.assertEqual(1, dummySpeedrun.startRace())

    def test_startRace_EnoughParticipantsAndEndArticle(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        dummySpeedrun.participants = ["Test", "Test2"]
        dummySpeedrun.endArticle = "dummyUrl"
        self.assertEqual(2, dummySpeedrun.startRace())

    def test_endRace_NotParticipant(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        dummySpeedrun.participants = ["Test", "Test2"]
        dummySpeedrun.startingTime = datetime.datetime.now()
        dummySpeedrun.endRace("Test3")
        self.assertEqual(None, dummySpeedrun.winner)

    def test_endRace_participant(self):
        dummySpeedrun = WikipediaSpeedrun.Speedrun()
        dummySpeedrun.participants = ["Test", "Test2"]
        dummySpeedrun.startingTime = datetime.datetime.now()
        expected = "Test"
        dummySpeedrun.endRace("Test")
        self.assertEqual(expected, dummySpeedrun.winner)