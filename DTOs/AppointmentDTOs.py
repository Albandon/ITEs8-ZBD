from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class AppointmentDTO(BaseModel):
    doctor_id: int
    patient_id: int
    treatment_id: int
    time: datetime
    room_id: int
    status: Literal["SCH", "CAN", "COM"]

    def map(self):
        return (
            self.doctor_id,
            self.patient_id,
            self.treatment_id,
            self.time,
            self.status,
            self.room_id,
        )