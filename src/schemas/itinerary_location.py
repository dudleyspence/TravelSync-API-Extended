from pydantic import BaseModel
from datetime import datetime

class ItineraryLocationBase(BaseModel):
    place_id: str


class ItineraryLocationResponse(ItineraryLocationBase):
    itinerary_id: int 
    id: int
    created_at: datetime
    order_index: int 

    class Config:
        orm_mode = True
