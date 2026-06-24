from fastapi import APIRouter, HTTPException
from db import get_write_conn, get_write_conn
import itertools
import Services.TreatmentService as Ts
from DTOs.TreatmentDTOs import Treatment as TDto

router = APIRouter(prefix="/treatments", tags=["Treatments"])

@router.get("/{treat_id}")
def get_treatment_by_id(t_id: int):
    con, pool = get_write_conn()
    try:
        result = Ts.get_treatment_by_id(con, t_id)
    finally:
        pool.putconn(con)

    return result

@router.get("/{treat_id}/time")
def get_treatment_time(t_id: int):
    con, pool = get_write_conn()
    try:
        result = Ts.get_treatment_time_by_id(con, t_id)
    finally:
        pool.putconn(con)

    return result

@router.post("/")
def create_treatment(data: TDto):
    con, pool = get_write_conn()
    try:
        result = Ts.create_treatment(con, data)
    finally:
        pool.putconn(con)

    return result

@router.patch("/{treat_id}/time/{time}")
def update_treatment_time(treat_id: int, time: int):
    con, pool = get_write_conn()
    try:
        result = Ts.update_treatment_time(treat_id, time)
    finally:
        pool.putconn(con)
    
    if not result:
        raise HTTPException(status_code=404, detail="update failed")

    return result