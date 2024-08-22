from pydantic import BaseModel
from datetime import datetime

class ItineraryBase(BaseModel):
    title: str
    group_id: int

class ItineraryCreate(ItineraryBase):
    pass

class ItineraryResponse(ItineraryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
