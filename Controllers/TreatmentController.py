from fastapi import APIRouter, HTTPException
import db
import Services.TreatmentService as Ts
from DTOs.TreatmentDTOs import Treatment as TDto

router = APIRouter(prefix="/treatments", tags=["Treatments"])

@router.get("/{treat_id}")
def get_treatment_by_id(t_id: int):
    con = db.get_connection()
    result = Ts.get_treatment_by_id(con, t_id)
    con.close()
    return result

@router.get("/{treat_id}/time")
def get_treatment_time(t_id: int):
    con = db.get_connection()
    result = Ts.get_treatment_time_by_id(con, t_id)
    con.close()
    return result

@router.post("/")
def create_treatment(data: TDto):
    con = db.get_connection()
    result = Ts.create_treatment(con, data)
    con.close()
    return result

@router.patch("/{treat_id}/time/{time}")
def update_treatment_time(treat_id: int, time: int):
    con = db.get_connection()
    result = Ts.update_treatment_time(treat_id, time)
    
    if not result:
        raise HTTPException(status_code=404, detail="update failed")
   
    con.close()
    return result