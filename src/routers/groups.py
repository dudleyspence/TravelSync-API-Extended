from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import GroupCreate, GroupResponse
from src.models import Group
from src.db.database import get_db

router = APIRouter()
