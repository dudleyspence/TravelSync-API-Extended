from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import UserCreate, UserResponse, UserWithGroupsResponse
from src.models import User
from src.db.database import get_db
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

router = APIRouter()

@router.get('/{user_id}', response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user  # SQLAlchemy model instance will be automatically converted to the Pydantic model

@router.post('/', response_model=UserResponse)
def post_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    new_user = User(
        email=user.email,
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  

    return new_user


# gets all the groups for a given user
@router.get('/{user_id}/groups', response_model=UserWithGroupsResponse)
def get_user_groups(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [membership.group for membership in user.group_members] 