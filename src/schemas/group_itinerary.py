from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class GroupItineraryBase(BaseModel):
    name: str
    group_itinerary_id: int
    itinerary_order: Optional[List[int]] = [] 


class GroupItineraryCreate(GroupItineraryBase):
    pass

class GroupItineraryUpdate(BaseModel):
    itinerary_order: List[int]

class GroupItineraryResponse(GroupItineraryBase):
    id: int
    join_code: str
    created_at: datetime

    class Config:
        orm_mode = True

class JoinGroupItineraryRequest(BaseModel):
    user_id: int
    join_code: str