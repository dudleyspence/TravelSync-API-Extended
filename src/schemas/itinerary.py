from pydantic import BaseModel
from datetime import datetime
from typing import List

class ItineraryBase(BaseModel):
    name: str

class ItineraryCreate(ItineraryBase):
    pass

class ItineraryUpdate(BaseModel):
    itinerary_order: List[int]

class ItineraryResponse(ItineraryBase):
    id: int
    join_code: str
    itinerary_order: List[int]
    created_at: datetime

    class Config:
        orm_mode = True

class JoinItineraryRequest(BaseModel):
    user_id: int
    join_code: str
