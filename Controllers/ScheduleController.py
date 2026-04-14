from fastapi import APIRouter, HTTPException
import db
import Services.ScheduleService as Scs
from DTOs.ScheduleDTOs import CreateScheduleRegularDTO, CreateScheduleModificationDTO

router = APIRouter(prefix="/schedules", tags=["Schedules"])

@router.post("/regular")
def create_regular_schedule(schedule: CreateScheduleRegularDTO):
    con = db.get_connection()
    try:
        Scs.create_regular_schedule(con, schedule)
    except Exception as e:
        con.close()
        raise HTTPException(status_code=400, detail=str(e))

    con.close()
    return {"message": "Regular schedule created"}

@router.put("/modify-day")
def modify_schedule_day(modified_day: CreateScheduleModificationDTO):
    con = db.get_connection()
    try:
        Scs.modify_schedule_single_day(con, modified_day)
    except ValueError as e:
        con.close()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        con.close()
        raise HTTPException(status_code=500, detail="Internal server error")

    con.close()
    return {"message": "Modified schedule for selected day"}

@router.put("/regular")
def update_regular_schedule(schedule: CreateScheduleRegularDTO):
    con = db.get_connection()
    try:
        Scs.update_regular_schedule(con, schedule)
    except ValueError as e:
        con.close()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        con.close()
        raise HTTPException(status_code=500, detail="Internal server error")

    con.close()
    return {"message": "Regular schedule updated"}

@router.get("/available")
def get_available_slots(doctor_id: int, treatment_id: int):
    con = db.get_connection()
    slots = Scs.get_available_slots(con, doctor_id, treatment_id)
    con.close()

    if slots is None:
        raise HTTPException(status_code=404, detail="Treatment not found")

    return slots