from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import os
from sqlalchemy.orm import Session
from src.schemas import FileResponse

from dotenv import load_dotenv

from src.models import File as FileModel  
from src.db.database import get_db

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

            # get type of the file
            file_type = mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'

            # Create a blob object in Firebase Storage
            blob = bucket.blob(f"{file_id}/{file.filename}")

            # Upload the file to Storage
            blob.upload_from_file(file.file, content_type=file.content_type)

            # Construct the file URL
            file_url = f"https://storage.googleapis.com/{bucket.name}/{file_id}/{file.filename}"

            # Create a new file record in the database
            new_file = FileModel(
                associated_id=itinerary_id,  
                filename=file.filename,
                file_type=file_type,
                file_url=file_url
            )

            # Add and commit the new file record to the database
            db.add(new_file)
            db.commit()
            db.refresh(new_file)

            return new_file

    except Exception as e:
        print(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload file")




# @router.delete('/delete_all/{itinerary_id}')
# def delete_all_files(itinerary_id: int):
#     blobs = bucket.list_blobs(prefix=f"{itinerary_id}/")
#     for blob in blobs:
#         blob.delete()
#     return {"message": "All files deleted successfully!"}
