from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


load_dotenv(".env.development")

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


engine = create_engine(DATABASE_URL) # Establishes a connection to the database (database must already exist for this)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # we use session to set these engine configurations and can use sessionlocal without having to repeat this config
# autocommit means changes to db arent automatically comitted, we have to commit the changes (safer that way)
# bind just binds the engine with the session (config) that we specified

Base = declarative_base() 
# creates a base class for all the SQLAlchemy models to inherit 
# By inheriting from Base, the model classes are automatically linked to SQLAlchemy, and they can be mapped to tables in the db



def get_db():
    db = SessionLocal()
    # this function generates a new instance of the session (db)
    # we create an instance of session each time we do a db request then close after
    try:
        yield db
    finally:
        db.close()

