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
