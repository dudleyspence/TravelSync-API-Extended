from pydantic import BaseModel

class FileBase(BaseModel):
    file_name: str
    itinerary_id: int
    file_type: str = None  
    file_path: str

class FileCreate(FileBase):
    pass

class FileResponse(FileBase):
    id: int
    file_type: str = None 
    file_path: str  

    class Config:
        orm_mode = True