from pydantic import BaseModel
from datetime import datetime

class ItineraryEventBase(BaseModel):
    itinerary_id: int
    name: str
    coords: str
    place_id: str
    order: int

class ItineraryEventCreate(ItineraryEventBase):
    pass

class ItineraryEventResponse(ItineraryEventBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
