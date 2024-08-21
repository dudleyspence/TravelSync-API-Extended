from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from src.db.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    email = Column(String(200), unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    created_at = Column(DateTime, default=func.now())


class Itinerary(Base):
    __tablename__ = 'itneraries'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=func.now())


class GroupMember(Base):
    __tablename__ = 'group_members'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)


class ItineraryEvent(Base):
    __tablename__ = 'itinerary_events'

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey('itineraries.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(200), nullable=False)
    coords = Column(String, nullable=False)
    place_id = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())

