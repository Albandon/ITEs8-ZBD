from fastapi import APIRouter
from db import get_write_conn, get_write_conn, run_in_threadpool
import Services.ClinicService as Cs
from DTOs.ClinicDTOs import Clinic as CDto

router = APIRouter(prefix="/clinics", tags=["Clinics"])

@router.get("/{clinic_id}")
async def get_clinic_by_id(clinic_id: int):
    con, pool = get_write_conn()
    try:
        result = await run_in_threadpool(Cs.get_clinic_by_id, con, clinic_id)
    finally:
        pool.putconn(con)

    return result

@router.post("/")
def create_clinic(clinic_data: CDto):
    con, pool = get_write_conn()
    try:
        result = Cs.create_clinic(con, clinic_data)
    finally:
        pool.putconn(con)

    return result

@router.post("/no_unique")
def create_clinic(clinic_data: CDto):
    con, pool = get_write_conn()
    try:
        result = Cs.create_clinic(con, clinic_data, False)
    finally:
        pool.putconn(con)

    return result

@router.get("/")
def get_all_clinics():
    con, pool = get_write_conn()
    try:
        result = Cs.get_all_clinics(con)
    finally:
        pool.putconn(con)

    return result