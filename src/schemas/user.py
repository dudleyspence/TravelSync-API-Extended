from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass 

class UserResponse(UserBase):
    pass

    class Config:
        orm_mode = True  
