from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from src.schemas import ItineraryCreate, ItineraryResponse, ItineraryEventCreate, ItineraryEventResponse, FileCreate, FileResponse, ItineraryUpdate
from src.models import Itinerary, ItineraryEvent, File as FileModel
from src.db.database import get_db
from typing import List
import pyrebase
import uuid

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



@router.post('/', response_model=ItineraryResponse)
def post_itinerary(itinerary: ItineraryCreate, db: Session = Depends(get_db)) -> ItineraryEventResponse:
    new_itinerary = Itinerary(**itinerary.model_dump())
    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)
    return new_itinerary



@router.get('/{itinerary_id}/events', response_model=List[ItineraryEventResponse])
def get_itinerary_events(itinerary_id: int, db: Session = Depends(get_db)) -> ItineraryEventResponse:
    db_itinerary_event = db.query(ItineraryEvent).filter(ItineraryEvent.itinerary_id == itinerary_id)
    print(db_itinerary_event)
    if db_itinerary_event is None:
        raise HTTPException(status_code=404, detail="Itinerary event not found")
    return db_itinerary_event 


@router.post('/{itinerary_id}/events', response_model=ItineraryResponse)
def add_itinerary_event(itinerary_id: int, event_data: ItineraryEventCreate, db: Session = Depends(get_db)) -> ItineraryResponse:
    # fetch the itinerary
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    # create new itinerary event
    new_event = ItineraryEvent(**event_data.model_dump(), itinerary_id=itinerary_id)
    db.add(new_event)
    db.commit()  # to generate ID for event event
    db.refresh(new_event)

    # update itinerary order
    if itinerary.itinerary_order:
        itinerary.itinerary_order.append(new_event.id)
    else:
        itinerary.itinerary_order = [new_event.id]
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
    
    unique_filename = f"{uuid.uuid4()}-{file.filename}"

    blob = storage.child(f"{itinerary_id}/{unique_filename}")
    blob.put(file.file)

    file_url = blob.get_url(None)

    new_file = FileModel(
        file_name=file.filename,
        itinerary_id=itinerary_id,
        file_path=file_url
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file

