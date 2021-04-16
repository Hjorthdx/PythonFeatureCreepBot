from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey
import Db


class User(Db.Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    up_votes = Column(Integer)
    down_votes = Column(Integer)
    preferred_work_timer = Column(Integer)
    preferred_break_timer = Column(Integer)
    #balance = Column(Integer) # For the casino cog is the current plan.

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, opdutter={self.up_votes}, neddutter={self.down_votes}, work/break timer={self.preferred_work_timer}/{self.preferred_break_timer}>\n"

    def __eq__(self, other):
        return isinstance(other, User) and other.id == self.id


class Pomodoro(Db.Base):
    __tablename__ = 'pomodoros'
    id = Column(Integer, primary_key=True)
    work_length = Column(Integer)
    break_length = Column(Integer)
    author = Column(BigInteger, ForeignKey('users.id'))
    starting_time = Column(DateTime)
