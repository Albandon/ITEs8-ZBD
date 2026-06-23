from fastapi import APIRouter, HTTPException
from db import get_read_conn, get_write_conn
import itertools
import Services.AppointmentService as As
import DTOs.AppointmentDTOs as Ads

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.get("/{appointment_id}")
def get_appointment_by_id(appointment_id: int):
    con, pool = get_read_conn()
    try:
        appointment = As.get_appointment_by_id(con, appointment_id)
    finally:
        pool.putconn(con)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment

@router.get("/patient/{patient_id}")
def get_by_patient(patient_id: int):
    con, pool = get_read_conn()
    try:
        appointments = As.get_appointments_by_patient_id(con, patient_id)
    finally:
        pool.putconn(con)

    return appointments

@router.post("/")
def add_appointment(appointment_data: Ads.AppointmentDTO):
    con, pool = get_write_conn()
    try:
        appointment = As.create_appointment(con, appointment_data)
    finally:
        pool.putconn(con)

    if not appointment:
        raise HTTPException(status_code=400, detail="Cannot book appointment")

    return True

@router.patch("/{appointment_id}/{status}")
def update_status(appointment_id: int, status: str):
    con, pool = get_write_conn()
    try:
        updated = As.update_appointment_status(con, appointment_id, status)
    finally:
        pool.putconn(con)

    if not updated:
        raise HTTPException(status_code=404, detail="update failed")

    return True