from fastapi import APIRouter, HTTPException

from utils.data import get_connection


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
