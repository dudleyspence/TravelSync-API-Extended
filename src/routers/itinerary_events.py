from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified  
from src.schemas import ItineraryEventResponse
from src.models import ItineraryEvent, GroupItinerary  
from src.db.database import get_db

router = APIRouter()

# delete an itinerary event
@router.delete('/{event_id}', response_model=ItineraryEventResponse)
def delete_event(event_id: int, db: Session = Depends(get_db)) -> ItineraryEventResponse:
    db_event = db.query(ItineraryEvent).filter(ItineraryEvent.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail='Event not found')

    # fetch itinerary
    itinerary = db.query(GroupItinerary).filter(GroupItinerary.id == db_event.group_itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Group itinerary not found")

    # update itinerary order/delete the event
    if itinerary.itinerary_order:
        try:
            itinerary.itinerary_order.remove(event_id)
            flag_modified(itinerary, "itinerary_order") 
        except ValueError:
            print("could not find id in event_order")
            pass

    db.delete(db_event)
    db.commit()

    db.commit()
    db.refresh(itinerary) 

    return db_event
