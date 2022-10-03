from fastapi import APIRouter, HTTPException
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


@router.get("/{user_id}")
async def read_user(user_id: int):
    con = get_connection()
    cur = con.execute("SELECT * FROM user WHERE id = (?)", (user_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="user not found")
    return dict(row)


@router.post("/")
async def create_user(user: User):
    con = get_connection()
    cur = con.execute("""INSERT INTO user(name, age, sex)
            VALUES(?, ?, ?)
            """, (user.name, user.age, user.sex,))
    cur.execute("SELECT * FROM user WHERE id = (?)", (cur.lastrowid,))
    row = cur.fetchone()
    con.commit()
    return dict(row)
