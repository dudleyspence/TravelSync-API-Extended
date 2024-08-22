from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import ItineraryEventCreate, ItineraryEventResponse
from src.models import ItineraryEvent
from src.db.database import get_db

router = APIRouter()


