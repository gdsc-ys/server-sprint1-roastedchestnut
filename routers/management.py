from fastapi import APIRouter, HTTPException, status
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
    cur.execute("SELECT * FROM management WHERE manager_id = (?) AND history_id = (?)", (management.manager_id, management.history_id,))
    row = cur.fetchone()
    con.commit()
    return dict(row)
    

@router.put("/{manager_id}/{history_id}")
async def update_management(manager_id: int, history_id: int, management: Management):
    con = get_connection()
    cur = con.execute("""UPDATE management
            SET type = (?)
            WHERE manager_id = (?) AND history_id = (?)
            """, (management.type, manager_id, history_id,))
    cur.execute("SELECT * FROM management WHERE manager_id = (?) AND history_id = (?)", (manager_id, history_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="management not found")
    con.commit()
    return dict(row)


@router.delete("/{manager_id}/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_management(manager_id: int, history_id: int):
    con = get_connection()
    cur = con.execute("DELETE FROM management WHERE manager_id = (?) AND history_id = (?)", (manager_id, history_id,))
    con.commit()
