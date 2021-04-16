import unittest
from unittest import mock
from models import User
from cogs import Karma
import discord
from discord.ext import commands


class TestKarma(unittest.TestCase):
    @mock.patch("Db.get_user_by_name", return_value=User(id=1, name="username_1"))
    def test__karma_name_str_id_none(self, mock_get_user_by_name):
        expected = User(id=1, name="username_1")
        result = Karma.Karma._karma(name="username_1", _id=None)
        self.assertEqual(result, expected)

    @mock.patch("Db.get_user_by_name", return_value=User(id=1, name="username_1"))
    def test__karma_name_str_id_int(self, mock_get_user_by_name):
        expected = User(id=1, name="username_1")
        result = Karma.Karma._karma(name="username_1", _id=1)
        self.assertEqual(result, expected)

    @mock.patch("Db.get_user_by_id", return_value=User(id=1, name="username_1"))
    def test__karma_name_none_id_int(self, mock_get_user_by_id):
        expected = User(id=1, name="username_1")
        result = Karma.Karma._karma(name=None, _id=1)
        self.assertEqual(result, expected)

    '''
    # Problem with the method that I gave as example is that it doesnt return anything, so how will this work?
    @mock.patch("Db.update_user_up_votes", return_value=User(id=1, name="username_1", up_votes=-2))
    def test__update_user_up_votes_same_author_and_user(self, mock_db_update_user_up_votes):
        expected = User(id=1, name="username_1", up_votes=-2)
        result = Karma.Karma._update_user_up_votes(1, 1, remove=False)
        self.assertEqual(result, expected)
    '''


if __name__ == '__main__':
    unittest.main()
