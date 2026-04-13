from datetime import datetime
from pydantic import BaseModel

class CreateDoctorDTO(BaseModel):
    first_name: str
    last_name: str
    sex: str

    def map(self):
        return (
            self.first_name,
            self.last_name,
            self.sex
        )

class SelectDoctorDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    sex: str

    def map(self):
        return (
            self.id,
            self.first_name,
            self.last_name,
            self.sex
        )

class SelectDoctorLoginInfoDTO(BaseModel):
    doctor_id: int
    email: str
    phone: str
    hash_password: str
    created_at: datetime

    def map(self):
        return (
            self.doctor_id,
            self.email,
            self.phone,
            self.hash_password,
            self.created_at
        )

class CreateDoctorLoginInfoDTO(BaseModel):
    doctor_id: int
    email: str
    phone: str
    password: str

    def map(self, hashed_password: str):
        return (
            self.doctor_id,
            self.email,
            self.phone,
            hashed_password
        )

class CreateDoctorWithLoginDTO(BaseModel):
    first_name: str
    last_name: str
    sex: str
    email: str
    phone: str
    password: str