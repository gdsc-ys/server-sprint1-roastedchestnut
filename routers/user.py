from fastapi import APIRouter, HTTPException

from utils.data import get_connection


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