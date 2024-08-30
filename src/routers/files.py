from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from src.schemas import FileCreate, FileResponse,   
from src.models import Itinerary, File as FileModel  
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


# Get the files for an itinerary
@router.get('/files/{itinerary_id}', response_model=List[FileResponse])
def get_files(itinerary_id: int, db: Session = Depends(get_db)) -> List[FileResponse]:
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()

    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    files = db.query(FileModel).filter(FileModel.itinerary_id == itinerary_id).all()

    return files




# Add a file to an itinerary
@router.post('/files/{itinerary_id}', response_model=FileResponse)
def post_file(itinerary_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)) -> FileResponse:
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()

    if not itinerary:
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


# Delete a file associated with an itinerary
@router.delete('/files/{itinerary_id}', response_model=FileResponse)
def delete_file(itinerary_id: int, file_id: int, db: Session = Depends(get_db)) -> FileResponse:
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")

    file_to_delete = db.query(FileModel).filter(FileModel.id == file_id, FileModel.itinerary_id == itinerary_id).first()
    if not file_to_delete:
        raise HTTPException(status_code=404, detail="File not found")

    db.delete(file_to_delete)
    db.commit()

    return file_to_delete
