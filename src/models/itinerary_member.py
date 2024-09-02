from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from src.db import Base


class ItineraryMember(Base):
    __tablename__ = 'itinerary_members'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(600), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    itinerary_id = Column(Integer, ForeignKey('itineraries.id', ondelete='CASCADE'), nullable=False)




