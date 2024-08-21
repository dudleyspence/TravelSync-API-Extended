import httpx
import src.models.SQLAlchemy_Models


async def create_users(user, db):
    db_user = src.models.SQLAlchemy_Models.User(**user.dict())
    db.add(user)
    db.commit(user)