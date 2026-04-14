from fastapi import APIRouter
import db
import Services.ClinicService as Cs
from DTOs.ClinicDTOs import Clinic as CDto

router = APIRouter(prefix="/clinics", tags=["Clinics"])

@router.get("/{clinic_id}")
def get_clinic_by_id(clinic_id: int):
    con = db.get_connection()
    result = Cs.get_clinic_by_id(con, clinic_id)
    con.close()
    return result

@router.post("/")
def create_clinic(clinic_data: CDto):
    con = db.get_connection()
    result = Cs.create_clinic(con, clinic_data)
    con.close()
    return result

@router.get("/")
def get_all_clinics():
    con = db.get_connection()
    result = Cs.get_all_clinics(con)
    con.close()
    return result