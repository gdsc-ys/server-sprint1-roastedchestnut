from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from utils.data import get_connection


class Vehicle(BaseModel):
    type: str
    status: str


router = APIRouter(
    prefix="/vehicle",
    tags=["vehicle"],
)


@router.get("/{vehicle_id}")
async def read_vehicle(vehicle_id: int):
    con = get_connection()
    cur = con.execute("SELECT * FROM vehicle WHERE id = (?)", (vehicle_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="vehicle not found")
    return dict(row)


@router.post("/")
async def create_vehicle(vehicle: Vehicle):
    con = get_connection()
    cur = con.execute("""INSERT INTO vehicle(type, status)
            VALUES(?, ?)
            """, (vehicle.type, vehicle.status,))
    cur.execute("SELECT * FROM vehicle WHERE id = (?)", (cur.lastrowid,))
    row = cur.fetchone()
    con.commit()
    return dict(row)
