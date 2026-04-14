from pydantic import BaseModel

class CreateRoomDTO(BaseModel):
    speciality_id: int
    clinic_id: int
    room_name: str

    def map(self):
        return (
            self.speciality_id,
            self.clinic_id,
            self.room_name
        )

class SelectRoomDTO(BaseModel):
    id: int
    speciality_id: int
    clinic_id: int
    room_name: str

    def map(self):
        return (
            self.id,
            self.speciality_id,
            self.clinic_id,
            self.room_name
        )