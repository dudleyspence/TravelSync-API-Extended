from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import ItineraryCreate, ItineraryResponse, ItineraryEventCreate, ItineraryEventResponse
from src.models import Itinerary
from src.models import ItineraryEvent
from src.db.database import get_db
from typing import List

router = APIRouter()

@router.get('/{itinerary_id}/itinerary-events', response_model=List[ItineraryEventResponse])
def get_itinerary_events(itinerary_id: int, db: Session = Depends(get_db)) -> ItineraryEventResponse:
    db_itinerary_event = db.query(ItineraryEvent).filter(ItineraryEvent.itinerary_id == itinerary_id)
    print(db_itinerary_event)
    if db_itinerary_event is None:
        raise HTTPException(status_code=404, detail="Itinerary event not found")
    return db_itinerary_event 


@router.post('/{itinerary_id}/itinerary-events', response_model=ItineraryEventResponse)
def post_itinerary_events(itinerary_id: int, itinerary_event: ItineraryEventCreate, db: Session = Depends(get_db)) -> ItineraryEventResponse:
    new_event = ItineraryEvent(**itinerary_event.dict(), itinerary_id=itinerary_id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event