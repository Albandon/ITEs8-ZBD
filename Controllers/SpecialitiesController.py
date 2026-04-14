from fastapi import APIRouter, HTTPException
import db
import Services.SpecialityService as Ss

router = APIRouter(prefix="/specialities", tags=["Specialities"])

@router.get("/{speciality_id}")
def get_speciality(speciality_id: int):
    con = db.get_connection()
    speciality = Ss.get_speciality_by_id(con, speciality_id)
    con.close()
    if not speciality:
        raise HTTPException(status_code=404, detail="Speciality not found")
    return speciality

@router.post("/")
def create_speciality(name: str):
    con = db.get_connection()
    speciality_id = Ss.create_speciality(con, name)
    con.close()
    if speciality_id == -1:
        raise HTTPException(status_code=409, detail="Speciality already exists")
    return {"speciality_id": speciality_id}

@router.post("/{speciality_id}/doctors/{doctor_id}")
def assign_to_doctor(speciality_id: int, doctor_id: int):
    con = db.get_connection()
    assigned = Ss.assign_speciality_to_doctor(con, speciality_id, doctor_id)
    con.close()
    if not assigned:
        raise HTTPException(status_code=409, detail="Speciality already assigned to doctor")
    return True