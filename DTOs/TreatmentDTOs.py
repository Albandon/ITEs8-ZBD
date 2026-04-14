from pydantic import BaseModel

class Treatment (BaseModel):
    name: str
    spec_id: str
    time_blocks: int
    
    def map(self):
        return (
            self.name,
            self.spec_id,
            self.time_blocks
        )