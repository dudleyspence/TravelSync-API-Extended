from pydantic import BaseModel

class ItineraryMemberBase(BaseModel):
    user_id: str
    itinerary_id: int  

class ItineraryMemberCreate(BaseModel):
    user_id: str

class ItineraryMemberResponse(ItineraryMemberBase):
    id: int

    class Config:
        orm_mode = True
