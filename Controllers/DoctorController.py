from fastapi import APIRouter, HTTPException
from db import get_read_conn, get_write_conn, primary_pool, _replica_cycle
import itertools
import Services.DoctorService as Ds
import DTOs.DoctorDTOs as DDs

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/search")
def search_by_name(query: str):
    con, pool = get_read_conn()
    try:
        doctors = Ds.search_doctors_by_name(con, query)
    finally:
        pool.putconn(con)

    return doctors

@router.get("/speciality/{speciality_id}")
def search_by_speciality(speciality_id: int):
    con, pool = get_read_conn()
    try:
        doctors = Ds.search_doctors_by_speciality_id(con, speciality_id)
    finally:
        pool.putconn(con)

    return doctors

@router.get("/{doctor_id}")
def get_doctor(doctor_id: int):
    con, pool = get_read_conn()
    try:
        doctor = Ds.get_doctor_by_id(con, doctor_id)
    finally:
        pool.putconn(con)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor

@router.post("/")
def create_doctor(doctor_data: DDs.CreateDoctorWithLoginDTO):
    con, pool = get_write_conn()
    try:
        doctor_id = Ds.create_doctor_with_login(con, doctor_data)
    finally:
        pool.putconn(con)

    return {"doctor_id": doctor_id}

@router.put("/{doctor_id}")
def update_doctor(doctor_id: int, doctor_data: DDs.CreateDoctorDTO):
    con, pool = get_write_conn()
    try:
        Ds.update_doctor(con, doctor_data)
    finally:
        pool.putconn(con)

    return True

@router.patch("/{doctor_id}/password")
def update_password(doctor_id: int, password: str):
    con, pool = get_write_conn()
    try:
        updated = Ds.update_doctor_password(con, password, doctor_id)
    finally:
        pool.putconn(con)

    if not updated:
        raise HTTPException(status_code=400, detail="New password must be different from old one")

    return True

@router.get("/{doctor_id}/login-info")
def get_login_info(doctor_id: int):
    con, pool = get_read_conn()
    try:
        info = Ds.get_doctor_login_info_by_doctor_id(con, doctor_id)
    finally:
        pool.putconn(con)

    if not info:
        raise HTTPException(status_code=404, detail="Login info not found")

    return info