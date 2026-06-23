from fastapi import APIRouter, HTTPException
from db import get_read_conn, get_write_conn, primary_pool, _replica_cycle
import itertools
import Services.SpecialityService as Ss

router = APIRouter(prefix="/specialities", tags=["Specialities"])

@router.get("/{speciality_id}")
def get_speciality(speciality_id: int):
    con, pool = get_read_conn()
    try:
        speciality = Ss.get_speciality_by_id(con, speciality_id)
    finally:
        pool.putconn(con)

    if not speciality:
        raise HTTPException(status_code=404, detail="Speciality not found")

    return speciality

@router.post("/")
def create_speciality(name: str):
    con, pool = get_write_conn()
    try:
        speciality_id = Ss.create_speciality(con, name)
    finally:
        pool.putconn(con)

    if speciality_id == -1:
        raise HTTPException(status_code=409, detail="Speciality already exists")

    return {"speciality_id": speciality_id}

@router.post("/{speciality_id}/doctors/{doctor_id}")
def assign_to_doctor(speciality_id: int, doctor_id: int):
    con, pool = get_write_conn()
    try:
        assigned = Ss.assign_speciality_to_doctor(con, speciality_id, doctor_id)
    finally:
        pool.putconn(con)

    if not assigned:
        raise HTTPException(status_code=409, detail="Speciality already assigned to doctor")

    return True