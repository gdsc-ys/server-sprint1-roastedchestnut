from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from utils.data import get_connection


class Management(BaseModel):
    manager_id: int
    history_id: int
    type: str


router = APIRouter(
    prefix="/management",
    tags=["management"],
)


@router.get("/manager/{manager_id}}")
async def read_management_manager(manager_id: int):
    con = get_connection()
    cur = con.execute("SELECT * FROM management WHERE manager_id = (?)", (manager_id,))
    rows = cur.fetchall()
    if rows is None:
        raise HTTPException(status_code=404, detail="management not found")
    return [dict(row) for row in rows]


@router.get("/history/{history_id}}")
async def read_management_history(history_id: int):
    con = get_connection()
    cur = con.execute("SELECT * FROM management WHERE history_id = (?)", (history_id,))
    rows = cur.fetchall()
    if rows is None:
        raise HTTPException(status_code=404, detail="management not found")
    return [dict(row) for row in rows]


@router.post("/")
async def create_management(management: Management):
    con = get_connection()
    cur = con.execute("""INSERT INTO management(manager_id, history_id, type)
            VALUES(?, ?, ?)
            """, (management.manager_id, management.history_id, management.type,))
    cur.execute("SELECT * FROM management WHERE manager_id = (?) and history_id = (?)", (management.manager_id, management.history_id,))
    row = cur.fetchone()
    con.commit()
    return dict(row)
    