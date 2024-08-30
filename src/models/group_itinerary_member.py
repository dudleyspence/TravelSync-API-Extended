from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from src.db import Base


class GroupItineraryMember(Base):
    __tablename__ = 'group_itinerary_members'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    group_itinerary_id = Column(Integer, ForeignKey('group_itineraries.id', ondelete='CASCADE'), nullable=False)




