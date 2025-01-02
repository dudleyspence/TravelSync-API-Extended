from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from src.schemas import ItineraryCreate, ItineraryResponse, ItineraryLocationResponse, ItineraryReorderRequest, ItinerarySummaryResponse
from src.models import Itinerary, ItineraryLocation, ItineraryMember
from src.db.database import get_db
from typing import List
from .utils import generate_join_code

router = APIRouter()


from fastapi import HTTPException

# Create a new itinerary
from pydantic import BaseModel


@router.post('', response_model=ItineraryResponse)
def create_itinerary(
    data: ItineraryCreate,
    db: Session = Depends(get_db)
) -> ItineraryResponse:
    join_code = generate_join_code()
    
    print(data)
    while db.query(Itinerary).filter(Itinerary.join_code == join_code).first() is not None:
        join_code = generate_join_code()

    new_itinerary = Itinerary(
        name=data.name,
        join_code=join_code
    )
    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)

    new_member = ItineraryMember(
        user_id=data.user_id,
        itinerary_id=new_itinerary.id
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_itinerary



# Gets an itinerary using an itinerary_id
@router.get('/{itinerary_id}', response_model=ItineraryResponse)
def get_itinerary(itinerary_id: int, db: Session = Depends(get_db)) -> ItineraryResponse:
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    return itinerary



# Returns all the locations currently in an itinerary
@router.get('/{itinerary_id}/locations', response_model=List[ItineraryLocationResponse])
def get_itinerary_locations(
    itinerary_id: int, 
    db: Session = Depends(get_db)
) -> List[ItineraryLocationResponse]:
    # Returns locations sorted by order_index
    db_locations = (
        db.query(ItineraryLocation)
        .filter(ItineraryLocation.itinerary_id == itinerary_id)
        .order_by(ItineraryLocation.order_index.asc())
        .all()
    )
    return db_locations



# Add a new event to the itinerary
@router.post("/{itinerary_id}/locations/{place_id}", response_model=ItineraryLocationResponse)
def add_itinerary_location(
    itinerary_id: int,
    place_id: str,
    db: Session = Depends(get_db)
) -> ItineraryLocationResponse:
    # Make sure itinerary exists
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    # Determine the next order_index
    new_largest_order_index = (
        db.query(ItineraryLocation.order_index)
        .filter(ItineraryLocation.itinerary_id == itinerary_id)
        .order_by(ItineraryLocation.order_index.desc())
        .first()
    )
    next_index = new_largest_order_index[0] + 1 if new_largest_order_index else 0

    new_location = ItineraryLocation(
        itinerary_id=itinerary_id,
        place_id=place_id,
        order_index=next_index,
    )
    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    return new_location


# using put not patch because we change/update the order of the intire itinerary
@router.put("/{itinerary_id}/reorder", response_model=List[ItineraryLocationResponse])
def reorder_itinerary_locations(
    itinerary_id: int,
    reorder_data: ItineraryReorderRequest,
    db: Session = Depends(get_db)
) -> List[ItineraryLocationResponse]:
    
    print(reorder_data)
    
    # using enumerate will give the index and the value of the ids
    # This means for each location we can set the order_index to be the index
    for index, loc_id in enumerate(reorder_data.location_ids_order):

        db.query(ItineraryLocation).filter(
            ItineraryLocation.id == loc_id,
            ItineraryLocation.itinerary_id == itinerary_id
        ).update({"order_index": index})
    db.commit()

    updated_locations = (
        db.query(ItineraryLocation)
        .filter(ItineraryLocation.itinerary_id == itinerary_id)
        .order_by(ItineraryLocation.order_index.asc())
        .all()
    )
    
    return updated_locations


# Delete an itinerary
@router.delete('/{itinerary_id}', response_model=ItineraryResponse)
def delete_itinerary(itinerary_id: int, db: Session = Depends(get_db)) -> ItineraryResponse:
    db_itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if db_itinerary is None:
        raise HTTPException(status_code=404, detail='Itinerary not found')

    db.delete(db_itinerary)
    db.commit()
    return db_itinerary







@router.get('/{itinerary_id}/summary', response_model=ItinerarySummaryResponse)
def get_itinerary_summary(itinerary_id: int, db: Session = Depends(get_db)) -> ItinerarySummaryResponse:
    # fetchinf the itinerary
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    # total locations in the itinerary
    total_locations = (
        db.query(func.count(ItineraryLocation.id))
        .filter(ItineraryLocation.itinerary_id == itinerary_id)
        .scalar()
    )
    # using scalar ensures a single scalar value is returned

    # total members in the itinerary
    total_members = (
        db.query(func.count(ItineraryMember.id))
        .filter(ItineraryMember.itinerary_id == itinerary_id)
        .scalar()
    )

    # summary response
    itinerary_summary = {
        "id": itinerary.id,
        "name": itinerary.name,
        "join_code": itinerary.join_code,
        "created_at": itinerary.created_at,
        "total_locations": total_locations,
        "total_members": total_members,
    }

    return itinerary_summary