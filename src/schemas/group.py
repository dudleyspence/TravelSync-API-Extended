from pydantic import BaseModel
from datetime import datetime
from typing import List


class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass


class GroupResponse(GroupBase):
    id: int
    created_at: datetime
    join_code: str


    class Config:
        orm_mode = True

class UserWithGroupsResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    groups: List[GroupBase]  # List of groups the user belongs to

    class Config:
        orm_mode = True


class JoinGroupRequest(BaseModel):
    user_id: int
    join_code: str