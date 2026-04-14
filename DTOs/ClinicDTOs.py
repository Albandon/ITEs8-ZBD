from pydantic import BaseModel

class Clinic(BaseModel):
    address: str
    city: str

    def map(self):
        return (
            self.address,
            self.city,
        )