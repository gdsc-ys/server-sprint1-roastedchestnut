from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from utils.data import get_connection


class Manager(BaseModel):
    name: str
    age: int
    sex: str
    admin: int


router = APIRouter(
    prefix="/manager",
    tags=["manager"],
)

con, cur = get_connection()


@router.get("/{manager_id}")
async def read_manager(manager_id: int):
    cur.execute("SELECT * FROM manager WHERE id = (?)", (manager_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="manager not found")
    return dict(row)


@router.post("/")
async def create_manager(manager: Manager):
    cur.execute("""INSERT INTO manager(name, age, sex, admin)
        VALUES(?, ?, ?, ?)
        """, (manager.name, manager.age, manager.sex, manager.admin,))
    cur.execute("SELECT * FROM manager WHERE id = (?)", (cur.lastrowid,))
    row = cur.fetchone()
    con.commit()
    return dict(row)
    

@router.put("/{manager_id}")
async def update_manager(manager_id: int, manager: Manager):
    cur.execute("""UPDATE manager
        SET name = (?), age = (?), sex = (?), admin = (?)
        WHERE id = (?)
        """, (manager.name, manager.age, manager.sex, manager.admin, manager_id,))
    cur.execute("SELECT * FROM manager WHERE id = (?)", (manager_id,))
    row = cur.fetchone()
    con.commit()
    return dict(row)


@router.delete("/{manager_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_manager(manager_id: int):
    cur.execute("DELETE FROM manager WHERE id = (?)", (manager_id,))
    con.commit()
