from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from src.schemas import GroupItineraryCreate, GroupItineraryResponse, ItineraryEventCreate, ItineraryEventResponse, FileCreate, FileResponse, GroupItineraryUpdate
from src.models import GroupItinerary, ItineraryEvent, File as FileModel
from src.db.database import get_db
from typing import List
import pyrebase

firebase_config = {
    "apiKey": "AIzaSyAnKhVLWe2wxmVZP5nwIPoiH7DLXIMevnM",
    "authDomain": "travelsync-e8555.firebaseapp.com",
    "projectId": "travelsync-e8555",
    "storageBucket": "travelsync-e8555.appspot.com",
    "messagingSenderId": "673531725643",
    "appId": "1:673531725643:web:f8a4d304cf94c443118ace",
    "measurementId": "G-3S0VBXVL5H",
    "databaseURL": ""  
}

firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()



router = APIRouter()


# Create new group itinerary
@router.post('/', response_model=GroupItineraryResponse)
def create_group_itinerary(itinerary: GroupItineraryCreate, db: Session = Depends(get_db)) -> GroupItineraryResponse:
    new_itinerary = GroupItinerary(**itinerary.model_dump())
    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)
    return new_itinerary


# returns all the events currently in an itinerary
@router.get('/{group_itinerary_id}/events', response_model=List[ItineraryEventResponse])
def get_itinerary_events(group_itinerary_id: int, db: Session = Depends(get_db)) -> ItineraryEventResponse:
    db_itinerary_event = db.query(ItineraryEvent).filter(ItineraryEvent.group_itinerary_id == group_itinerary_id)
    print(db_itinerary_event)
    if db_itinerary_event is None:
        raise HTTPException(status_code=404, detail="Itinerary event not found")
    return db_itinerary_event 


# Add a new event to the itinerary
@router.post('/{group_itinerary_id}/events', response_model=GroupItineraryResponse)
def add_itinerary_event(group_itinerary_id: int, event_data: ItineraryEventCreate, db: Session = Depends(get_db)) -> GroupItineraryResponse:
    itinerary = db.query(GroupItinerary).filter(GroupItinerary.id == group_itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    new_event = ItineraryEvent(**event_data.model_dump(), group_itinerary_id=group_itinerary_id)
    db.add(new_event)
    db.commit()  # to generate ID for event event
    db.refresh(new_event)

    # update itinerary order
    if itinerary.itinerary_order:
        itinerary.itinerary_order.append(new_event.id)
        print(itinerary.itinerary_order)
    else:
        itinerary.itinerary_order = [new_event.id]

    flag_modified(itinerary, "itinerary_order")

    db.commit()
    db.refresh(itinerary)


    return itinerary


@router.get('/{itinerary_id}', response_model=ItineraryResponse)
def get_itinerary(itinerary_id: int, db: Session = Depends(get_db)) -> ItineraryResponse:

    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    return itinerary


@router.patch('/{itinerary_id}', response_model=ItineraryResponse)
def reorder_itinerary_events(itinerary_id: int, itinerary_update: ItineraryUpdate, db: Session = Depends(get_db)) -> ItineraryEventResponse:

    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()

    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    itinerary.itinerary_order = itinerary_update.itinerary_order

    db.commit()
    db.refresh(itinerary)
    return itinerary



@router.get('/{itinerary_id}/files', response_model=List[FileResponse])
def get_files(itinerary_id: int, db: Session = Depends(get_db)) -> List[FileResponse]:
    db_event = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    files = db.query(FileModel).filter(FileModel.itinerary_id == itinerary_id).all()

    return files


@router.post('/{itinerary_id}/files', response_model=FileResponse)
def post_file(itinerary_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)) -> FileResponse:
    db_event = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    blob = storage.child(f"{file.filename}")
    blob.put(file.file)

    file_url = blob.get_url(None)

    new_file = FileModel(
        file_name=file.filename,
        itinerary_id=itinerary_id,
        file_path=file_url.replace("/?alt=media", "").rstrip("/")
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file


@router.delete('/{itinerary_id}/files', response_model=FileResponse)
def delete_file(itinerary_id: int, file_id: int, db: Session = Depends(get_db)) -> FileResponse:
    db_event = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    file_delete = db.query(FileModel).filter(FileModel.id == file_id, FileModel.itinerary_id == itinerary_id).first()
    if not file_delete:
        raise HTTPException(status_code=404, detail="File not found")

    db.delete(file_delete)
    db.commit()

    return file_delete