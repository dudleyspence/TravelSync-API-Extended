from pydantic import BaseModel
from datetime import datetime
from typing import List

class ItineraryBase(BaseModel):
    name: str

class ItineraryCreate(ItineraryBase):
    pass

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
    location_ids: List[int]