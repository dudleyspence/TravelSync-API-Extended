#create users
#get users
#update users
#delete users

from fastapi import APIRouter, HTTPException, Request
from src.models.users_models import create_users


router = APIRouter()

@router.post('/users')
async def post_users(id, username, email, password):
    response = await create_users(id, username, email, password)