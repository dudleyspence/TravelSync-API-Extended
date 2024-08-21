#create groups
#get groups
#update groups
#delete groups

from fastapi import APIRouter, HTTPException, Request


router = APIRouter()
@router.post('/places/info')