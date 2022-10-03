from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from utils.data import get_connection


class History(BaseModel):
    user_id: int
    vehicle_id: int
    start_date: str
    end_date: str


router = APIRouter(
    prefix="/history",
    tags=["history"],
)

con, cur = get_connection()


@router.get("/{history_id}")
async def read_history(history_id: int):
    cur.execute("SELECT * FROM history WHERE id = (?)", (history_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="history not found")
    return dict(row)


@router.get("/user/{user_id}")
async def read_history_user(user_id: int):
    cur.execute("SELECT * FROM history WHERE user_id = (?)", (user_id,))
    rows = cur.fetchall()
    if rows is None:
        raise HTTPException(status_code=404, detail="history not found")
    return [dict(row) for row in rows]


@router.get("/vehicle/{vehicle_id}")
async def read_history_vehicle(vehicle_id: int):
    cur.execute("SELECT * FROM history WHERE vehicle_id = (?)", (vehicle_id,))
    rows = cur.fetchall()
    if rows is None:
        raise HTTPException(status_code=404, detail="history not found")
    return [dict(row) for row in rows]


@router.post("/")
async def create_history(history: History):
    cur.execute("""INSERT INTO history(user_id, vehicle_id, start_date, end_date)
        VALUES(?, ?, ?, ?)
        """, (history.user_id, history.vehicle_id, history.start_date, history.end_date,))
    cur.execute("SELECT * FROM history WHERE id = (?)", (cur.lastrowid,))
    row = cur.fetchone()
    con.commit()
    return dict(row)
    

@router.put("/{history_id}")
async def update_history(history_id: int, history: History):
    cur.execute("""UPDATE history
        SET user_id = (?), vehicle_id = (?), start_date = (?), end_date = (?)
        WHERE id = (?)
        """, (history.user_id, history.vehicle_id, history.start_date, history.end_date, history_id,))
    cur.execute("SELECT * FROM history WHERE id = (?)", (history_id,))
    row = cur.fetchone()
    con.commit()
    if row is None:
        raise HTTPException(status_code=404, detail="history not found")
    return dict(row)


@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_history(history_id: int):
    cur.execute("DELETE FROM history WHERE id = (?)", (history_id,))
    con.commit()
