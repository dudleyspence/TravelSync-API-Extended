from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import ItineraryCreate, ItineraryResponse
from src.models import Itinerary
from src.db.database import get_db

router = APIRouter()
