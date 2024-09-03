from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
import os
from sqlalchemy.orm import Session
from src.schemas import FileResponse

from dotenv import load_dotenv

from src.models import File as FileModel  
from src.db.database import get_db
from typing import List


import uuid
import mimetypes

import firebase_admin
from firebase_admin import credentials, storage

ENV = os.getenv("FASTAPI_ENV", "development")
if ENV == "development":
    load_dotenv(".env.firebase")

firebase_cred_info = {
    "type": os.getenv("firebase_type"), 
    "project_id": os.getenv("firebase_project_id"),
    "private_key_id": os.getenv("firebase_private_key_id"),
    "private_key": os.getenv("firebase_private_key").replace('\\n', '\n'),
    "client_email": os.getenv("firebase_client_email"),
    "client_id": os.getenv("firebase_client_id"),
    "auth_uri": os.getenv("firebase_auth_uri"),
    "token_uri": os.getenv("firebase_token_uri"),
    "auth_provider_x509_cert_url": os.getenv("firebase_auth_provider_x509_cert_url"),
    "client_x509_cert_url": os.getenv("firebase_client_x509_cert_url"),
    "universe_domain": os.getenv("firebase_universe_domain"),
}


firebase_bucket_name = os.getenv("firebase_storage_bucket")


cred = credentials.Certificate(firebase_cred_info)
firebase_admin.initialize_app(cred, {
    'storageBucket': firebase_bucket_name
})

bucket = storage.bucket()


router = APIRouter()

@router.post('/upload/{itinerary_id}', response_model=FileResponse)
def upload_file(itinerary_id: int, file: UploadFile = File(...), db: Session = Depends(get_db))-> FileResponse:
    try:    
            print(file)
            # unique ID for the file
            file_id = str(uuid.uuid4())

            file_type = mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'

            blob = bucket.blob(f"{file_id}/{file.filename}")

            # Upload the file to Storage
            blob.upload_from_file(file.file, content_type=file.content_type)

            # construct file URL
            file_url = f"https://storage.googleapis.com/{bucket.name}/{file_id}/{file.filename}"

            # create new file in database
            new_file = FileModel(
                itinerary_id=itinerary_id,  
                file_name=file.filename,
                file_type=file_type,
                file_path=file_url
            )

            db.add(new_file)
            db.commit()
            db.refresh(new_file)

            return new_file

    except Exception as e:
        print(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload file")


# Get all files for an itinerary
@router.get('/{itinerary_id}', response_model=List[FileResponse])
def get_itinerary_files(itinerary_id: int, db: Session = Depends(get_db)) -> List[FileResponse]:
    files = db.query(FileModel).filter(FileModel.itinerary_id == itinerary_id).all()    
    return files



@router.delete('/{file_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_itinerary_file(file_id: int, db: Session = Depends(get_db)):
    file_to_delete = db.query(FileModel).filter(FileModel.id == file_id).first()
    
    if file_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    try:
        # the .replace just removes our baseURL/bucketname from the full path to only give the relative path
        print(f"Full file path: {file_to_delete.file_path}")
        print(f"Bucket name: {bucket.name}")
        file_path = file_to_delete.file_path.replace(f"https://storage.googleapis.com/{bucket.name}/", "")
        blob = bucket.blob(file_path)
        blob.delete() 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete file from storage")
    

     

# @router.delete('/delete_all/{itinerary_id}')
# def delete_all_files(itinerary_id: int):
#     blobs = bucket.list_blobs(prefix=f"{itinerary_id}/")
#     for blob in blobs:
#         blob.delete()
#     return {"message": "All files deleted successfully!"}
