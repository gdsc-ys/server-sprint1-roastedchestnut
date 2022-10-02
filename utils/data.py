import sqlite3

def get_connection():
    con = sqlite3.connect("rental.db")
    con.row_factory = sqlite3.Row
    return con

def close_connection(con):
    con.close()
