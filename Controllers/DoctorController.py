from fastapi import APIRouter, HTTPException
import db
import Services.DoctorService as Ds
import DTOs.DoctorDTOs as DDs

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/search")
def search_by_name(query: str):
    con = db.get_connection()
    doctors = Ds.search_doctors_by_name(con, query)
    con.close()
    return doctors

@router.get("/speciality/{speciality_id}")
def search_by_speciality(speciality_id: int):
    con = db.get_connection()
    doctors = Ds.search_doctors_by_speciality_id(con, speciality_id)
    con.close()
    return doctors

@router.get("/{doctor_id}")
def get_doctor(doctor_id: int):
    con = db.get_connection()
    doctor = Ds.get_doctor_by_id(con, doctor_id)
    con.close()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.post("/")
def create_doctor(doctor_data: DDs.CreateDoctorWithLoginDTO):
    con = db.get_connection()
    doctor_id = Ds.create_doctor_with_login(con, doctor_data)
    con.close()
    return {"doctor_id": doctor_id}

@router.put("/{doctor_id}")
def update_doctor(doctor_id: int, doctor_data: DDs.CreateDoctorDTO):
    con = db.get_connection()
    Ds.update_doctor(con, doctor_data)
    con.close()
    return True

@router.patch("/{doctor_id}/password")
def update_password(doctor_id: int, password: str):
    con = db.get_connection()
    updated = Ds.update_doctor_password(con, password, doctor_id)
    con.close()
    if not updated:
        raise HTTPException(status_code=400, detail="New password must be different from old one")
    return True

@router.get("/{doctor_id}/login-info")
def get_login_info(doctor_id: int):
    con = db.get_connection()
    info = Ds.get_doctor_login_info_by_doctor_id(con, doctor_id)
    con.close()
    if not info:
        raise HTTPException(status_code=404, detail="Login info not found")
    return info