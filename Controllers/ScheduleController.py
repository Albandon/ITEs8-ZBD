from fastapi import APIRouter, HTTPException
from db import get_write_conn, get_write_conn
import itertools
import Services.ScheduleService as Scs
from DTOs.ScheduleDTOs import CreateScheduleRegularDTO, CreateScheduleModificationDTO

router = APIRouter(prefix="/schedules", tags=["Schedules"])

@router.post("/regular")
def create_regular_schedule(schedule: CreateScheduleRegularDTO):
    con, pool = get_write_conn()
    try:
        Scs.create_regular_schedule(con, schedule)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        pool.putconn(con)

    return {"message": "Regular schedule created"}

@router.put("/modify-day")
def modify_schedule_day(modified_day: CreateScheduleModificationDTO):
    con, pool = get_write_conn()
    try:
        Scs.modify_schedule_single_day(con, modified_day)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        pool.putconn(con)

    return {"message": "Modified schedule for selected day"}

@router.put("/regular")
def update_regular_schedule(schedule: CreateScheduleRegularDTO):
    con, pool = get_write_conn()
    try:
        Scs.update_regular_schedule(con, schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        pool.putconn(con)

    return {"message": "Regular schedule updated"}

@router.get("/available")
def get_available_slots(doctor_id: int, treatment_id: int):
    con, pool = get_write_conn()
    try:
        slots = Scs.get_available_slots(con, doctor_id, treatment_id)
    finally:
        pool.putconn(con)

    if slots is None:
        raise HTTPException(status_code=404, detail="Treatment not found")

    return slots