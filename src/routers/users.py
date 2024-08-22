from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import UserCreate, UserResponse
from src.models import User
from src.db.database import get_db

router = APIRouter()
