from fastapi import APIRouter, HTTPException
import db
import Services.RoomService as Rs
import DTOs.RoomDTOs as RDs

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/{room_id}")
def get_room(room_id: int):
    con = db.get_connection()
    room = Rs.get_room_by_id(con, room_id)
    con.close()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.get("/speciality/{speciality_id}")
def get_rooms_by_speciality(speciality_id: int):
    con = db.get_connection()
    rooms = Rs.get_rooms_by_speciality_id(con, speciality_id)
    con.close()
    return rooms

@router.get("/clinic/{clinic_id}")
def get_rooms_by_clinic(clinic_id: int):
    con = db.get_connection()
    rooms = Rs.get_rooms_by_clinic_id(con, clinic_id)
    con.close()
    return rooms

@router.get("/clinic/{clinic_id}/speciality/{speciality_id}")
def get_rooms_by_clinic_speciality(clinic_id: int, speciality_id: int):
    con = db.get_connection()
    rooms = Rs.get_rooms_by_clinic_and_speciality_id(con, clinic_id, speciality_id)
    con.close()
    return rooms

@router.post("/")
def create_room(room_data: RDs.CreateRoomDTO):
    con = db.get_connection()
    room_id = Rs.create_room(con, room_data)
    con.close()
    return {"room_id": room_id}


