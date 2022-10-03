from fastapi import APIRouter, HTTPException

from utils.data import get_connection


router = APIRouter(
    prefix="/manager",
    tags=["manager"],
)


@router.get("/{manager_id}")
async def read_manager(manager_id: int):
    con = get_connection()
    cur = con.execute("SELECT * FROM manager WHERE id = (?)", (manager_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="manager not found")
    return dict(row)
