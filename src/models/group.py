from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from src.db import Base


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    created_at = Column(DateTime, default=func.now())


class GroupMember(Base):
    __tablename__ = 'group_members'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)