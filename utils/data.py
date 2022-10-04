import sqlite3
import redis


# enable foreign key constraint
def get_connection():
    con = sqlite3.connect("rental.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    return con, cur


def close_connection(con):
    con.close()


def get_redis_connection():
    r = redis.Redis(decode_responses=True)
    return r


# use this instead of sqlite3.Row 
# to use serialization of dictionary 
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
