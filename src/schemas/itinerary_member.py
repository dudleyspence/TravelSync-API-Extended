from pydantic import BaseModel

class ItineraryMemberBase(BaseModel):
    user_id: int
    itinerary_id: int  # Updated field name

class ItineraryMemberCreate(BaseModel):
    user_id: int

class ItineraryMemberResponse(ItineraryMemberBase):
    id: int

    class Config:
        orm_mode = True
