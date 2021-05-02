# Repository pattern possible here ?
# Seperate tables a bit more in the models
# To something more like this perhabs:
# User table som refer til både 0->* pomodoro tables, som indeholder pomodoro data ofc.
# User table har så også et 1->1 til et preferred time table som indeholder de der to tider.
# User table har så også idk
# Tabte den lige lidt.
# Min tanke er bare her at det hele handler jo omkring Users for alle de der metoder, så det er svært at adskille det af
#

import os
from dotenv import load_dotenv

load_dotenv()
from sqlalchemy import create_engine, update, func, desc, asc, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from models import *

engine = create_engine(os.getenv("DB_CONNECTION_STRING"), pool_pre_ping=True, echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_user_by_id(_id):
    return session.query(User).filter_by(id=_id).first()


def get_user_by_name(name):
    return session.query(User).filter_by(name=name).first()


def get_amount_of_users(amount):
    return session.query(User)[0:amount]


def update_user_up_votes(_id, amount):
    session.query(User).filter(User.id == _id).update({User.up_votes: User.up_votes + amount},
                                                      synchronize_session=False)
    session.commit()


def update_user_down_votes(_id, amount):
    session.query(User).filter(User.id == _id).update({User.down_votes: User.down_votes + amount},
                                                      synchronize_session=False)
    session.commit()


def get_highest_up_votes():
    return session.query(User).order_by(User.up_votes.desc()).first()


def get_highest_down_votes():
    return session.query(User).order_by(User.up_votes.desc()).first()


def add_pomodoro_to_db(work_length, break_length, author_id, starting_time):
    session.add(Pomodoro(work_length=work_length, break_length=break_length, author=author_id, starting_time=starting_time))
    session.commit()


def get_preferred_work_and_break_timer(_id):
    user = session.query(User).filter_by(id=_id).first()
    return user.preferred_work_timer, user.preferred_break_timer


def update_preferred_work_and_break_timer(_id, preferred_work_timer, preferred_break_timer):
    session.query(User).filter(User.id == _id).update({User.preferred_work_timer: preferred_work_timer,
                                                       User.preferred_break_timer: preferred_break_timer},
                                                      synchronize_session=False)
    session.commit()
