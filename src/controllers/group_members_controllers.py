#add member to group
#get group members
#delete member from group

from fastapi import APIRouter, HTTPException, Request


router = APIRouter()
@router.post()