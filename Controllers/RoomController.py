from fastapi import APIRouter, HTTPException
from db import get_write_conn, get_write_conn
import itertools
import Services.RoomService as Rs
import DTOs.RoomDTOs as RDs

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/{room_id}")
def get_room(room_id: int):
    con, pool = get_write_conn()
    try:
        room = Rs.get_room_by_id(con, room_id)
    finally:
        pool.putconn(con)

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    return room

@router.get("/speciality/{speciality_id}")
def get_rooms_by_speciality(speciality_id: int):
    con, pool = get_write_conn()
    try:
        rooms = Rs.get_rooms_by_speciality_id(con, speciality_id)
    finally:
        pool.putconn(con)

    return rooms

@router.get("/clinic/{clinic_id}")
def get_rooms_by_clinic(clinic_id: int):
    con, pool = get_write_conn()
    try:
        rooms = Rs.get_rooms_by_clinic_id(con, clinic_id)
    finally:
        pool.putconn(con)

    return rooms

@router.get("/clinic/{clinic_id}/speciality/{speciality_id}")
def get_rooms_by_clinic_speciality(clinic_id: int, speciality_id: int):
    con, pool = get_write_conn()
    try:
        rooms = Rs.get_rooms_by_clinic_and_speciality_id(con, clinic_id, speciality_id)
    finally:
        pool.putconn(con)

    return rooms

@router.post("/")
def create_room(room_data: RDs.CreateRoomDTO):
    con, pool = get_write_conn()
    try:
        room_id = Rs.create_room(con, room_data)
    finally:
        pool.putconn(con)

    return {"room_id": room_id}


