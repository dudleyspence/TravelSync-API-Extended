from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=true, index=True)
    username = Column(String(100), unique=True)
    email = Column(String(200), unique=True)
    created_at = Column(DateTime, default=func.now())

