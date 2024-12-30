from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified  
from src.schemas import ItineraryLocationResponse
from src.models import ItineraryLocation, Itinerary  
from src.db.database import get_db

router = APIRouter()

# delete an itinerary location
@router.delete('/{location_id}', response_model=ItineraryLocationResponse)
def delete_location(location_id: int, db: Session = Depends(get_db)) -> ItineraryLocationResponse:
    db_location = db.query(ItineraryLocation).filter(ItineraryLocation.id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail='Location not found')

    # fetch itinerary
    itinerary = db.query(Itinerary).filter(Itinerary.id == db_location.itinerary_id).first()  
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    # update itinerary order/delete the event
    if itinerary.itinerary_order:
        try:
            itinerary.itinerary_order.remove(location_id)
            flag_modified(itinerary, "itinerary_order")
        except ValueError:
            print("Could not find event_id in itinerary_order")
            pass

    db.delete(db_location)
    db.commit()
    db.refresh(itinerary) 

    return db_location

