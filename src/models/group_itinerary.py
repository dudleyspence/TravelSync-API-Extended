from sqlalchemy import JSON, Column, Integer, String, DateTime, func, ForeignKey
from src.db import Base


class GroupItinerary(Base):
    __tablename__ = 'group_itineraries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    join_code = Column(String(10), unique=True, nullable=False, index=True)
    itinerary_order = Column(JSON, default=[])
    created_at = Column(DateTime, default=func.now())




