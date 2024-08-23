from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import ItineraryEventCreate, ItineraryEventResponse
from src.models import ItineraryEvent
from src.db.database import get_db

router = APIRouter()

@router.delete('/{event_id}', response_model=ItineraryEventResponse)
def delete_event(event_id: int, db: Session = Depends(get_db)) -> ItineraryEventResponse:
    db_event = db.query(ItineraryEvent).filter(ItineraryEvent.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail='Event not found')
    db.delete(db_event)
    db.commit()
    return db_event