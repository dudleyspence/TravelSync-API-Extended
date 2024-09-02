from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from src.db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    email = Column(String(200), unique=True)
    created_at = Column(DateTime, default=func.now())


