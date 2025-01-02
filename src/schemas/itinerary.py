from pydantic import BaseModel
from datetime import datetime
from typing import List

class ItineraryBase(BaseModel):
    name: str

class ItineraryCreate(ItineraryBase):
    user_id: int

class ItineraryResponse(ItineraryBase):
    id: int
    join_code: str
    created_at: datetime

    class Config:
        orm_mode = True

class JoinItineraryRequest(BaseModel):
    user_id: str
    join_code: str

class ItineraryReorderRequest(BaseModel):
    location_ids_order: List[int]


class ItinerarySummaryResponse(BaseModel):
    id: int
    name: str
    join_code: str
    created_at: datetime
    total_locations: int
    total_members: int

    class Config:
        orm_mode = True