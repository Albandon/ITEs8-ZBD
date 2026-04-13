from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class AppointmentDTO(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    treatment_id: int
    time: datetime
    room_id: int
    status: Literal["SCH", "CAN", "COM"]

    def map(self):
        return (
            self.id,
            self.doctor_id,
            self.patient_id,
            self.treatment_id,
            self.time,
            self.room_id,
            self.status,
        )