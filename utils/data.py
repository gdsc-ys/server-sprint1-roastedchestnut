import sqlite3


# enable foreign key constraint
def get_connection():
    con = sqlite3.connect("rental.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    return con, cur


def close_connection(con):
    con.close()
