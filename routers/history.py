from fastapi import APIRouter, HTTPException

from utils.data import get_connection


router = APIRouter(
    prefix="/history",
    tags=["history"],
)


@router.get("/{history_id}")
async def read_history(history_id: int):
    con = get_connection()
    cur = con.execute("SELECT * FROM history WHERE id = (?)", (history_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="history not found")
    return dict(row)


@router.get("/user/{user_id}")
async def read_history_user(user_id: int):
    con = get_connection()
    cur = con.execute("SELECT * FROM history WHERE user_id = (?)", (user_id,))
    rows = cur.fetchall()
    if rows is None:
        raise HTTPException(status_code=404, detail="history not found")
    return [dict(row) for row in rows]


@router.get("/user/{vehicle_id}")
async def read_history_user(vehicle_id: int):
    con = get_connection()
    cur = con.execute("SELECT * FROM history WHERE vehicle_id = (?)", (vehicle_id,))
    rows = cur.fetchall()
    if rows is None:
        raise HTTPException(status_code=404, detail="history not found")
    return [dict(row) for row in rows]
