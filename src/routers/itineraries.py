from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from src.schemas import ItineraryCreate, ItineraryResponse, ItineraryEventCreate, ItineraryEventResponse, ItineraryUpdate  
from src.models import Itinerary, ItineraryEvent
from src.db.database import get_db
from typing import List
from .utils import generate_join_code

router = APIRouter()


# Create new itinerary
@router.post('', response_model=ItineraryResponse)
def create_itinerary(itinerary: ItineraryCreate, db: Session = Depends(get_db)) -> ItineraryResponse:
    join_code = generate_join_code()

    # check for unique join code
    while db.query(Itinerary).filter(Itinerary.join_code == join_code).first() is not None:
        join_code = generate_join_code()

    new_itinerary = Itinerary(
        name=itinerary.name,
        join_code=join_code
    )

    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)
    return new_itinerary

# Returns all the events currently in an itinerary
@router.get('/{itinerary_id}/events', response_model=List[ItineraryEventResponse])
def get_itinerary_events(itinerary_id: int, db: Session = Depends(get_db)) -> List[ItineraryEventResponse]:
    db_itinerary_events = db.query(ItineraryEvent).filter(ItineraryEvent.itinerary_id == itinerary_id).all()
    if not db_itinerary_events:
        raise HTTPException(status_code=404, detail="Itinerary events not found")
    return db_itinerary_events


# Add a new event to the itinerary
@router.post('/{itinerary_id}/events', response_model=ItineraryResponse)
def add_itinerary_event(itinerary_id: int, event_data: ItineraryEventCreate, db: Session = Depends(get_db)) -> ItineraryResponse:
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    new_event = ItineraryEvent(**event_data.model_dump(), itinerary_id=itinerary_id)
    db.add(new_event)
    db.commit()  # to generate ID for event
    db.refresh(new_event)

    # Update itinerary order
    if itinerary.itinerary_order:
        itinerary.itinerary_order.append(new_event.id)
    else:
        itinerary.itinerary_order = [new_event.id]

    flag_modified(itinerary, "itinerary_order")
    db.commit()
    db.refresh(itinerary)

    return itinerary

# Gets an itinerary using an itinerary_id
@router.get('/{itinerary_id}', response_model=ItineraryResponse)
def get_itinerary(itinerary_id: int, db: Session = Depends(get_db)) -> ItineraryResponse:
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    return itinerary


# Update itinerary order
@router.patch('/{itinerary_id}', response_model=ItineraryResponse)
def reorder_itinerary_events(itinerary_id: int, itinerary_update: ItineraryUpdate, db: Session = Depends(get_db)) -> ItineraryResponse:
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()

    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    itinerary.itinerary_order = itinerary_update.itinerary_order

    db.commit()
    db.refresh(itinerary)
    return itinerary



# Delete an itinerary
@router.delete('/{itinerary_id}', response_model=ItineraryResponse)
def delete_itinerary(itinerary_id: int, db: Session = Depends(get_db)) -> ItineraryResponse:
    db_itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if db_itinerary is None:
        raise HTTPException(status_code=404, detail='Itinerary not found')

    db.delete(db_itinerary)
    db.commit()
    return db_itinerary