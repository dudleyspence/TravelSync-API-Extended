from sqlalchemy import JSON, Column, Integer, String, DateTime, func
from src.db import Base


class Itinerary(Base):
    __tablename__ = 'itineraries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    join_code = Column(String(10), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())




