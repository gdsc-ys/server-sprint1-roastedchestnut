from http.client import USE_PROXY
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from utils.data import get_connection


class User(BaseModel):
    name: str
    age: int
    sex: str


router = APIRouter(
    prefix="/user",
    tags=["user"],
)

con, cur = get_connection()


@router.get("/{user_id}")
async def read_user(user_id: int):
    cur.execute("SELECT * FROM user WHERE id = (?)", (user_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="user not found")
    return dict(row)


@router.post("/")
async def create_user(user: User):
    cur.execute("""INSERT INTO user(name, age, sex)
        VALUES(?, ?, ?)
        """, (user.name, user.age, user.sex,))
    cur.execute("SELECT * FROM user WHERE id = (?)", (cur.lastrowid,))
    row = cur.fetchone()
    con.commit()
    return dict(row)


@router.put("/{user_id}")
async def update_user(user_id: int, user: User):
    cur.execute("""UPDATE user
        SET name = (?), age = (?), sex = (?)
        WHERE id = (?)
        """, (user.name, user.age, user.sex, user_id,))
    cur.execute("SELECT * FROM user WHERE id = (?)", (user_id,))
    row = cur.fetchone()
    con.commit()
    return dict(row)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    cur.execute("DELETE FROM user WHERE id = (?)", (user_id,))
    con.commit()
