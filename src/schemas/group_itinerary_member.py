from pydantic import BaseModel

class GroupItineraryMemberBase(BaseModel):
    user_id: int
    group_itineray_id: int

class GroupItineraryMemberCreate(BaseModel):
    user_id: int

class GroupItineraryMemberResponse(GroupItineraryMemberBase):
    id: int

    class Config:
        orm_mode = True

