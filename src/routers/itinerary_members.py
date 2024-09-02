from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import ItineraryMemberCreate, ItineraryMemberResponse, UserResponse, JoinItineraryRequest  
from src.models import ItineraryMember, Itinerary, User  # Updated imports
from src.db.database import get_db
from typing import List

router = APIRouter()

# Gets all the members of an itinerary
@router.get('/{itinerary_id}/members', response_model=List[UserResponse])
def get_users_in_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return [member.user for member in itinerary.members]

# Joins a user to an itinerary
@router.post('/join', response_model=ItineraryMemberResponse)
def join_itinerary(request: JoinItineraryRequest, db: Session = Depends(get_db)) -> ItineraryMemberResponse:

    print(request)
    itinerary = db.query(Itinerary).filter(Itinerary.join_code == request.join_code).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Invalid join code")

    # Check if the user exists in the database
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    # Check if the user is already a member of the itinerary
    existing_member = db.query(ItineraryMember).filter(
        ItineraryMember.itinerary_id == itinerary.id,
        ItineraryMember.user_id == request.user_id
    ).first()

    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member of the itinerary")

    # Add user to the itinerary
    new_itinerary_member = ItineraryMember(user_id=request.user_id, itinerary_id=itinerary.id)

    db.add(new_itinerary_member)
    db.commit()
    db.refresh(new_itinerary_member)

    return new_itinerary_member

# Deletes a member from an itinerary
@router.delete('/{itinerary_id}/members/{user_id}', response_model=ItineraryMemberResponse)
def delete_member_from_itinerary(itinerary_id: int, user_id: int, db: Session = Depends(get_db)) -> ItineraryMemberResponse:
    db_member = db.query(ItineraryMember).filter(ItineraryMember.user_id == user_id, ItineraryMember.itinerary_id == itinerary_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail='Itinerary member not found')
    db.delete(db_member)
    db.commit()
    return db_member
