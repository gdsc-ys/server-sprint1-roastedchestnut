from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from utils.data import get_connection


class Vehicle(BaseModel):
    type: str
    status: str


router = APIRouter(
    prefix="/vehicle",
    tags=["vehicle"],
)

con, cur = get_connection()


@router.get("/{vehicle_id}")
async def read_vehicle(vehicle_id: int):
    cur.execute("SELECT * FROM vehicle WHERE id = (?)", (vehicle_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="vehicle not found")
    return dict(row)


@router.post("/")
async def create_vehicle(vehicle: Vehicle):
    cur.execute("""INSERT INTO vehicle(type, status)
        VALUES(?, ?)
        """, (vehicle.type, vehicle.status,))
    cur.execute("SELECT * FROM vehicle WHERE id = (?)", (cur.lastrowid,))
    row = cur.fetchone()
    con.commit()
    return dict(row)


@router.put("/{vehicle_id}")
async def update_vehicle(vehicle_id: int, vehicle: Vehicle):
    cur.execute("""UPDATE vehicle
        SET type = (?), status = (?)
        WHERE id = (?)
        """, (vehicle.type, vehicle.status, vehicle_id,))
    cur.execute("SELECT * FROM vehicle WHERE id = (?)", (vehicle_id,))
    row = cur.fetchone()
    con.commit()
    return dict(row)


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(vehicle_id: int):
    cur.execute("DELETE FROM vehicle WHERE id = (?)", (vehicle_id,))
    con.commit()
