import os
from dotenv import load_dotenv

load_dotenv()
from sqlalchemy import create_engine, update, func, desc, asc, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from models import *

engine = create_engine(os.getenv("TEST_CONNECT"), pool_pre_ping=True, echo=True)
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




# OLD UNDER
import asyncio
import os

import asyncpg


async def myfetch(query):
    conn = await asyncpg.connect(user='postgres', password='MD80N2N!fuHz', database='DiscordData', host='127.0.0.1')
    values = await conn.fetch(query)
    await conn.close()
    return values


# Perhabs ? I'm not sure what is best. Both seem, I mean not so safe. Sql injection xd
async def add_opdut(query):
    sql_query = "UPDATE users SET opdutter = opdutter + 1 WHERE id=" + query
    pgpass = os.getenv("PG_PASSWORD")
    conn = await asyncpg.connect(user='postgres', password=pgpass, database='DiscordData', host='127.0.0.1')
    res = await conn.fetch(sql_query)
    await conn.close()
    return res
