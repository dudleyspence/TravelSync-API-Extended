from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ItineraryBase(BaseModel):
    name: str
    itinerary_id: int  # Updated field name
    itinerary_order: Optional[List[int]] = []

class ItineraryCreate(ItineraryBase):
    pass

class ItineraryUpdate(BaseModel):
    itinerary_order: List[int]

class ItineraryResponse(ItineraryBase):
    id: int
    join_code: str
    created_at: datetime

    class Config:
        orm_mode = True

class JoinItineraryRequest(BaseModel):
    user_id: int
    join_code: str
