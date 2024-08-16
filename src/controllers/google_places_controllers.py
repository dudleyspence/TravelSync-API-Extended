from models.google_places_models import fetch_nearby_places, fetch_place_info
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post('/places/info')
async def get__place_info(address:str):
    try:
        info = await fetch_place_info(address)
        return {"info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@router.post('/places/nearby')
async def get_nearby_places(location: str, radius: int, type="tourist_attraction"):
    try:
        locations = await fetch_nearby_places(location, radius, type)
        return {"locations": locations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

