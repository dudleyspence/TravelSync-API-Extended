from src.models.google_places_models import fetch_nearby_places, fetch_place_info, fetch_place_detail
from fastapi import APIRouter, HTTPException, Request


router = APIRouter()
@router.post('/info')
async def get_place_info(request: Request):
    body = await request.json()
    address = body.get("addressStr", None)
    place_id = body.get("place_id", None)

    try:
        if place_id:
            response = await fetch_place_info(place_id=place_id)
        else:
            response = await fetch_place_info(address=address)

        return {"placeInfo": response}

    except HTTPException as err:
        raise err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@router.post('/nearby')
async def get_nearby_places(location: str, radius=2000, type="tourist_attraction"):
    try:
        response = await fetch_nearby_places(location, radius, type)
        return {"locations": response}
    except HTTPException as err:
        print(err)
        raise err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@router.post('/detail')
async def get_place_detail(place_id: str):
    try:
        response = await fetch_place_detail(place_id)
        return {"details": response}
    except HTTPException as err:
        raise err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
