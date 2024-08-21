#create users
#get users
#update users
#delete users

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr
from src.db.database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from src.models.users_models import create_users

class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    created_at: int

def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter()

@router.post('/users')
async def post_users():
    await create_users(UserBase, db_dependency)