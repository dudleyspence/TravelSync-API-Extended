from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import ItineraryCreate, ItineraryResponse, ItineraryEventCreate, ItineraryEventResponse, ItineraryUpdate
from src.models import Itinerary
from src.models import ItineraryEvent
from src.db.database import get_db
from typing import List

router = APIRouter()



@router.post('/', response_model=ItineraryResponse)
def post_itinerary(itinerary: ItineraryCreate, db: Session = Depends(get_db)) -> ItineraryEventResponse:
    new_itinerary = Itinerary(**itinerary.model_dump())
    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)
    return new_itinerary



@router.get('/{itinerary_id}/itinerary-events', response_model=List[ItineraryEventResponse])
def get_itinerary_events(itinerary_id: int, db: Session = Depends(get_db)) -> ItineraryEventResponse:
    db_itinerary_event = db.query(ItineraryEvent).filter(ItineraryEvent.itinerary_id == itinerary_id)
    print(db_itinerary_event)
    if db_itinerary_event is None:
        raise HTTPException(status_code=404, detail="Itinerary event not found")
    return db_itinerary_event 


@router.post('/{itinerary_id}/itinerary-events', response_model=ItineraryEventResponse)
def post_itinerary_events(itinerary_id: int, itinerary_event: ItineraryEventCreate, db: Session = Depends(get_db)) -> ItineraryEventResponse:
    new_event = ItineraryEvent(**itinerary_event.model_dump(), itinerary_id=itinerary_id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@router.patch('/{itinerary_id}', response_model=ItineraryResponse)
def reorder_itinerary_events(itinerary_id: int, itinerary_update: ItineraryUpdate, db: Session = Depends(get_db)) -> ItineraryEventResponse:

    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()

    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    itinerary.itinerary_order = itinerary_update.itinerary_order

    db.commit()
    db.refresh(itinerary)
    return itinerary