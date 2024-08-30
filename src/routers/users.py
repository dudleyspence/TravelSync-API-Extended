from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import UserCreate, UserLogin, UserResponse, GroupItineraryResponse
from src.models import User, GroupItineraryMember
from src.db.database import get_db
from typing import List
from .utils import verify_password, hash_password



router = APIRouter()

# login user
@router.post('/user', response_model=UserResponse)
def get_user(user: UserLogin, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user is None or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=404, detail="Invalid email or password")
    return db_user


# add a new user
@router.post('/', response_model=UserResponse)
def post_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    new_user = User(
        email=user.email,
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  

    return new_user


# gets all group itineraries for a user
@router.get('/{user_id}/group_itineraries', response_model=List[GroupItineraryResponse])
def get_user_groups(user_id: int, db: Session = Depends(get_db)):
    group_itinerary_memberships = db.query(GroupItineraryMember).filter(GroupItineraryMember.user_id == user_id).all()
    
    if not group_itinerary_memberships:
        raise HTTPException(status_code=404, detail="User not found or no group itineraries found")

    return group_itineraries