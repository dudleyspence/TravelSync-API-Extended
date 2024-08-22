#create itinerary
#get itinerary
#update itinerary
#delete itinerary

from fastapi import APIRouter, HTTPException, Request


router = APIRouter()
@router.post('/places/info')