from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import UserCreate, UserResponse, ItineraryResponse 
from src.models import User, ItineraryMember, Itinerary
from src.db.database import get_db
from typing import List
from .utils import verify_password, hash_password

router = APIRouter()


# add a new user
@router.post('/', response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    new_user = User(
        id=user.id,
        email=user.email,
        name=user.name,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  

    return new_user

# gets all itineraries for a user
@router.get('/{user_id}/itineraries', response_model=List[ItineraryResponse])  
def get_user_itineraries(user_id: str, db: Session = Depends(get_db)):
    itinerary_memberships = db.query(ItineraryMember).filter(ItineraryMember.user_id == user_id).all()

    #  making a loop that extracts into a list the itinerary_ids for all the itineraries this user is a member of
    itinerary_ids = [membership.itinerary_id for membership in itinerary_memberships]

    itineraries = db.query(Itinerary).filter(Itinerary.id.in_(itinerary_ids)).all()

    return itineraries  


# get all details for one user 
@router.get('/{user_id}', response_model=UserResponse)  
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found in database")

    return user  